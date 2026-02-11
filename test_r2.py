"""
R2 Connection Test Script
"""
import os
import sys

# 환경변수 확인
print("=== 환경변수 확인 ===")
print(f"R2_ACCOUNT_ID: {os.environ.get('R2_ACCOUNT_ID', 'NOT SET')}")
print(f"R2_ACCESS_KEY: {os.environ.get('R2_ACCESS_KEY', 'NOT SET')}")
print(f"R2_SECRET_KEY: {'SET' if os.environ.get('R2_SECRET_KEY') else 'NOT SET'}")
print(f"R2_BUCKET_NAME: {os.environ.get('R2_BUCKET_NAME', 'NOT SET')}")
print()

try:
    from r2_client import R2Client

    print("=== R2 연결 시도 ===")
    client = R2Client()
    print("✅ R2 클라이언트 연결 성공!")
    print()

    # 버킷 존재 확인
    print("=== 버킷 목록 ===")
    try:
        response = client.s3_client.list_buckets()
        buckets = [b['Name'] for b in response.get('Buckets', [])]
        for bucket in buckets:
            print(f"  - {bucket}")
    except Exception as e:
        print(f"❌ 버킷 목록 실패: {e}")

    print()

    # 파일 목록 확인
    print("=== 파일 목록 (최대 100개) ===")
    files = list(client.list_files("", max_keys=100))
    if files:
        for f in files[:20]:  # 처음 20개만 표시
            print(f"  📄 {f['key']} ({f['size']} bytes)")
        if len(files) > 20:
            print(f"  ... 외 {len(files) - 20}개 파일")
    else:
        print("  (파일 없음)")

    print()
    print(f"총 {len(files)}개 파일 찾음")

except Exception as e:
    print(f"❌ 오류: {e}")
    import traceback
    traceback.print_exc()

input("\n엔터를 누르면 종료...")
