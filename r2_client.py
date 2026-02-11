"""
KBJ2 R2 Cloud Storage Client
Cloudflare R2 (S3 Compatible) File Management
"""
import os
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from typing import List, Dict, Optional, Generator
from datetime import datetime, timedelta
from pathlib import Path


class R2Client:
    """Cloudflare R2 Storage Client with File Explorer Interface"""

    def __init__(
        self,
        account_id: str = None,
        access_key: str = None,
        secret_key: str = None,
        bucket_name: str = "kbj2-storage"
    ):
        self.account_id = account_id or os.environ.get("R2_ACCOUNT_ID")
        self.access_key = access_key or os.environ.get("R2_ACCESS_KEY")
        self.secret_key = secret_key or os.environ.get("R2_SECRET_KEY")
        self.bucket_name = bucket_name or os.environ.get("R2_BUCKET_NAME", "kbj2-storage")

        if not all([self.account_id, self.access_key, self.secret_key]):
            raise ValueError("R2 credentials not provided. Set R2_ACCOUNT_ID, R2_ACCESS_KEY, R2_SECRET_KEY env vars.")

        self.s3_client = boto3.client(
            service_name='s3',
            endpoint_url=f"https://{self.account_id}.r2.cloudflarestorage.com",
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=Config(signature_version='s3v4'),
            region_name='auto'
        )

    # ============================================================
    # BUCKET MANAGEMENT
    # ============================================================

    def create_bucket(self) -> bool:
        """Create bucket if not exists"""
        try:
            self.s3_client.create_bucket(Bucket=self.bucket_name)
            print(f"   Bucket '{self.bucket_name}' created")
            return True
        except ClientError as e:
            if e.response['Error']['Code'] in ['BucketAlreadyOwnedByYou', 'BucketAlreadyExists']:
                print(f"   Bucket '{self.bucket_name}' already exists")
                return True
            print(f"   Error creating bucket: {e}")
            return False

    def setup_cors(self, allowed_origins: List[str] = None) -> bool:
        """Setup CORS for bucket"""
        if allowed_origins is None:
            allowed_origins = ['*']

        cors_config = {
            'CORSRules': [{
                'AllowedHeaders': ['*'],
                'AllowedMethods': ['GET', 'PUT', 'POST', 'DELETE', 'HEAD'],
                'AllowedOrigins': allowed_origins,
                'ExposeHeaders': ['ETag'],
                'MaxAgeSeconds': 3600
            }]
        }
        try:
            self.s3_client.put_bucket_cors(Bucket=self.bucket_name, CORSConfiguration=cors_config)
            print(f"   CORS configured for {self.bucket_name}")
            return True
        except Exception as e:
            print(f"   CORS setup failed: {e}")
            return False

    # ============================================================
    # FILE OPERATIONS
    # ============================================================

    def upload_file(
        self,
        local_path: str,
        r2_key: str = None,
        metadata: Dict = None
    ) -> bool:
        """Upload single file to R2"""
        local_path = Path(local_path)
        if not local_path.exists():
            raise FileNotFoundError(f"File not found: {local_path}")

        if r2_key is None:
            r2_key = local_path.name

        extra_args = {}
        if metadata:
            extra_args['Metadata'] = metadata

        try:
            self.s3_client.upload_file(
                str(local_path),
                self.bucket_name,
                r2_key,
                ExtraArgs=extra_args
            )
            return True
        except Exception as e:
            print(f"Upload failed: {e}")
            return False

    def upload_dir(
        self,
        local_dir: str,
        r2_prefix: str = "",
        pattern: str = "*",
        progress_callback=None
    ) -> Dict[str, int]:
        """Upload directory recursively"""
        local_dir = Path(local_dir)
        if not local_dir.exists():
            raise FileNotFoundError(f"Directory not found: {local_dir}")

        results = {"uploaded": 0, "failed": 0, "skipped": 0}
        files = list(local_dir.rglob(pattern))

        for i, file in enumerate(files):
            if file.is_file():
                relative_path = file.relative_to(local_dir)
                r2_key = f"{r2_prefix}/{relative_path}".replace("\\", "/").lstrip("/")

                if self.upload_file(file, r2_key):
                    results["uploaded"] += 1
                else:
                    results["failed"] += 1

                if progress_callback:
                    progress_callback(i + 1, len(files), str(file))

        return results

    def download_file(self, r2_key: str, local_path: str = None) -> bool:
        """Download file from R2"""
        if local_path is None:
            local_path = Path(r2_key).name

        local_path = Path(local_path)
        local_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            self.s3_client.download_file(
                self.bucket_name,
                r2_key,
                str(local_path)
            )
            return True
        except Exception as e:
            print(f"Download failed: {e}")
            return False

    def download_dir(
        self,
        r2_prefix: str,
        local_dir: str,
        progress_callback=None
    ) -> Dict[str, int]:
        """Download all files with prefix"""
        local_dir = Path(local_dir)
        local_dir.mkdir(parents=True, exist_ok=True)

        results = {"downloaded": 0, "failed": 0}
        files = list_files(r2_prefix)

        for i, file_info in enumerate(files):
            local_path = local_dir / file_info['key'].replace(r2_prefix, "").lstrip("/")
            if self.download_file(file_info['key'], local_path):
                results["downloaded"] += 1
            else:
                results["failed"] += 1

            if progress_callback:
                progress_callback(i + 1, len(files), file_info['key'])

        return results

    def delete_file(self, r2_key: str) -> bool:
        """Delete file from R2"""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=r2_key)
            return True
        except Exception as e:
            print(f"Delete failed: {e}")
            return False

    def delete_prefix(self, r2_prefix: str) -> int:
        """Delete all files with prefix"""
        deleted = 0
        for obj in self.list_objects(r2_prefix):
            if self.delete_file(obj['Key']):
                deleted += 1
        return deleted

    # ============================================================
    # FILE LISTING
    # ============================================================

    def list_objects(
        self,
        prefix: str = "",
        max_keys: int = 1000,
        delimiter: str = ""
    ) -> List[Dict]:
        """List objects in bucket"""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix,
                MaxKeys=max_keys,
                Delimiter=delimiter
            )

            objects = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    objects.append({
                        'key': obj['Key'],
                        'size': obj['Size'],
                        'last_modified': obj['LastModified'],
                        'etag': obj['ETag'].strip('"')
                    })

            return objects
        except ClientError as e:
            print(f"List failed: {e}")
            return []

    def list_files(self, prefix: str = "") -> Generator[Dict, None, None]:
        """Yield files matching prefix (handles pagination)"""
        continuation_token = None

        while True:
            kwargs = {
                'Bucket': self.bucket_name,
                'Prefix': prefix,
                'MaxKeys': 1000
            }
            if continuation_token:
                kwargs['ContinuationToken'] = continuation_token

            try:
                response = self.s3_client.list_objects_v2(**kwargs)
            except ClientError:
                break

            if 'Contents' in response:
                for obj in response['Contents']:
                    yield {
                        'key': obj['Key'],
                        'size': obj['Size'],
                        'last_modified': obj['LastModified'],
                        'etag': obj['ETag'].strip('"')
                    }

            if not response.get('IsTruncated'):
                break

            continuation_token = response.get('NextContinuationToken')

    def list_folders(self, prefix: str = "") -> List[str]:
        """List common prefixes (folders)"""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix,
                Delimiter='/',
                MaxKeys=1000
            )

            folders = []
            if 'CommonPrefixes' in response:
                for p in response['CommonPrefixes']:
                    folder = p['Prefix'].rstrip('/')
                    if folder:
                        folders.append(folder)

            return folders
        except ClientError:
            return []

    # ============================================================
    # SIGNED URLS
    # ============================================================

    def get_signed_url(
        self,
        r2_key: str,
        expiration: int = 3600
    ) -> Optional[str]:
        """Generate presigned URL for download"""
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': r2_key},
                ExpiresIn=expiration
            )
            return url
        except Exception as e:
            print(f"Signed URL generation failed: {e}")
            return None

    def get_upload_url(
        self,
        r2_key: str,
        expiration: int = 3600
    ) -> Optional[str]:
        """Generate presigned URL for upload"""
        try:
            url = self.s3_client.generate_presigned_url(
                'put_object',
                Params={'Bucket': self.bucket_name, 'Key': r2_key},
                ExpiresIn=expiration
            )
            return url
        except Exception as e:
            print(f"Upload URL generation failed: {e}")
            return None

    # ============================================================
    # FILE INFO
    # ============================================================

    def get_file_info(self, r2_key: str) -> Optional[Dict]:
        """Get file metadata"""
        try:
            response = self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=r2_key
            )
            return {
                'key': r2_key,
                'size': response['ContentLength'],
                'last_modified': response['LastModified'],
                'etag': response['ETag'].strip('"'),
                'content_type': response.get('ContentType', 'application/octet-stream'),
                'metadata': response.get('Metadata', {})
            }
        except ClientError:
            return None

    def file_exists(self, r2_key: str) -> bool:
        """Check if file exists"""
        return self.get_file_info(r2_key) is not None

    def get_bucket_size(self) -> int:
        """Get total bucket size in bytes"""
        total = 0
        for obj in self.list_files():
            total += obj['size']
        return total


# ============================================================
# CLI INTERFACE
# ============================================================

def main():
    """CLI interface for R2 operations"""
    import argparse

    parser = argparse.ArgumentParser(description="KBJ2 R2 Cloud Storage Manager")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Upload
    up_parser = subparsers.add_parser("upload", help="Upload files/directories")
    up_parser.add_argument("path", help="Local file or directory path")
    up_parser.add_argument("--key", help="R2 key (destination)")
    up_parser.add_argument("--prefix", default="", help="R2 prefix for directory upload")

    # Download
    down_parser = subparsers.add_parser("download", help="Download files")
    down_parser.add_argument("key", help="R2 file key")
    down_parser.add_argument("--dest", help="Local destination path")

    # List
    ls_parser = subparsers.add_parser("ls", help="List files")
    ls_parser.add_argument("--prefix", default="", help="R2 prefix to list")
    ls_parser.add_argument("--folders", action="store_true", help="List folders only")

    # Delete
    rm_parser = subparsers.add_parser("rm", help="Delete files")
    rm_parser.add_argument("key", help="R2 file key to delete")

    # URL
    url_parser = subparsers.add_parser("url", help="Generate signed URL")
    url_parser.add_argument("key", help="R2 file key")
    url_parser.add_argument("--expires", type=int, default=3600, help="Expiration in seconds")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    client = R2Client()

    if args.command == "upload":
        path = Path(args.path)
        if path.is_file():
            success = client.upload_file(args.path, args.key)
            print(f"Upload: {'OK' if success else 'FAILED'}")
        elif path.is_dir():
            results = client.upload_dir(args.path, args.prefix)
            print(f"Uploaded: {results['uploaded']}, Failed: {results['failed']}")

    elif args.command == "download":
        success = client.download_file(args.key, args.dest)
        print(f"Download: {'OK' if success else 'FAILED'}")

    elif args.command == "ls":
        if args.folders:
            folders = client.list_folders(args.prefix)
            for f in folders:
                print(f"  {f}/")
        else:
            for obj in client.list_files(args.prefix):
                print(f"  {obj['key']} ({obj['size']} bytes)")

    elif args.command == "rm":
        success = client.delete_file(args.key)
        print(f"Delete: {'OK' if success else 'FAILED'}")

    elif args.command == "url":
        url = client.get_signed_url(args.key, args.expires)
        print(f"Signed URL (expires {args.expires}s): {url}")


if __name__ == "__main__":
    main()
