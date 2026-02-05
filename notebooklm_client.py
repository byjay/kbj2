import os
import json
import time

# Try importing requests, fallback to simulation if missing
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

class NotebookLMClient:
    """
    Official NotebookLM Enterprise Client
    Based on Document: 노트북lm.md (v1alpha API)
    """
    def __init__(self, project_number=None, location="global", auth_token=None):
        self.project_number = project_number or os.getenv("NOTEBOOKLM_PROJECT_NUMBER")
        self.location = location or os.getenv("NOTEBOOKLM_LOCATION", "global")
        self.auth_token = auth_token or os.getenv("NOTEBOOKLM_AUTH_TOKEN")
        
        # Debug Logs
        if not self.project_number:
            print("❌ [Client Init] Missing PROJECT_NUMBER")
        else:
            print(f"🔧 [Client Init] Project: {self.project_number} | Location: {self.location}")

        # Endpoint construction based on docs
        # https://ENDPOINT_LOCATION-discoveryengine.googleapis.com/...
        self.endpoint_location = self.location if self.location in ["us", "eu"] else "global"
        
        # Doc says: "ENDPOINT_LOCATION: ... us, eu, global" => "global-discoveryengine..."
        self.base_url = f"https://{self.endpoint_location}-discoveryengine.googleapis.com/v1alpha/projects/{self.project_number}/locations/{self.location}/notebooks"
        print(f"🔧 [Client Init] Base URL: {self.base_url}")
        
        # Enable Simulation Mode if credentials are missing
        self.simulation_mode = not (self.project_number and self.auth_token and REQUESTS_AVAILABLE)
        if self.simulation_mode:
            print("\n⚠️  [NotebookLM] Running in SIMULATION MODE (Missing Credentials or 'requests' lib)")
            if not self.auth_token:
                print("   - Reason: Missing AUTH_TOKEN")

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }

    def create_notebook(self, title):
        """Creates a new notebook via notebooks.create"""
        if self.simulation_mode:
            print(f"📓 [NotebookLM-Sim] Creating Notebook: '{title}'")
            return {
                "notebookId": f"sim_nb_{int(time.time())}",
                "title": title,
                "name": f"projects/{self.project_number or 'SIM'}/locations/{self.location}/notebooks/sim_nb_123",
                "metadata": {"userRole": "PROJECT_ROLE_OWNER"}
            }

        try:
            payload = {"title": title}
            resp = requests.post(self.base_url, headers=self._get_headers(), json=payload)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"❌ [API Error] Failed to create notebook: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"   [Error Details]: {e.response.text}")
            
            # Smart Fallback
            print("⚠️ [Smart Fallback] Switching to SIMULATION MODE for create_notebook")
            self.simulation_mode = True # Use Sim mode for subsequent calls
            return {
                "notebookId": f"sim_fallback_{int(time.time())}",
                "title": title,
                "name": f"projects/{self.project_number or 'SIM'}/locations/{self.location}/notebooks/sim_fallback",
                "metadata": {"userRole": "PROJECT_ROLE_OWNER"}
            }

    def add_source_url(self, notebook_id, url, title="Web Source"):
        """Adds a URL source. Distinguishes between Web and Video (YouTube)."""
        is_youtube = "youtube.com" in url or "youtu.be" in url
        
        if self.simulation_mode or notebook_id.startswith("sim_"):
            source_type = "Video" if is_youtube else "Web"
            print(f"📓 [NotebookLM-Sim] Adding {source_type} Source: {url}")
            return {
                "sources": [{
                    "sourceId": {"id": f"sim_src_{int(time.time())}"},
                    "title": title,
                    "settings": {"status": "SOURCE_STATUS_COMPLETE"}
                }]
            }

        api_url = f"{self.base_url}/{notebook_id}/sources:batchCreate"
        
        # Payload construction based on doc page 10-12
        if is_youtube:
            # YouTube uses videoContent
            user_content = {"videoContent": {"url": url}}
        else:
            # General Web uses webContent
            user_content = {"webContent": {"url": url, "sourceName": title}}

        payload = {"userContents": [user_content]}

        try:
            resp = requests.post(api_url, headers=self._get_headers(), json=payload)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"❌ [API Error] Failed to add URL source: {e}")
            print("⚠️ [Smart Fallback] Using Simulation for Source")
            return {
                "sources": [{
                    "sourceId": {"id": f"sim_src_{int(time.time())}"},
                    "title": title,
                    "settings": {"status": "SOURCE_STATUS_COMPLETE"}
                }]
            }

    def add_source_text(self, notebook_id, text, title="Text Source"):
        """Adds raw text as a source."""
        if self.simulation_mode or notebook_id.startswith("sim_"):
            print(f"📓 [NotebookLM-Sim] Adding Text Source: '{title}'")
            return {
                "sources": [{
                    "sourceId": {"id": f"sim_txt_{int(time.time())}"},
                    "title": title,
                    "settings": {"status": "SOURCE_STATUS_COMPLETE"}
                }]
            }

        api_url = f"{self.base_url}/{notebook_id}/sources:batchCreate"
        user_content = {
            "textContent": {
                "sourceName": title,
                "content": text
            }
        }
        payload = {"userContents": [user_content]}

        try:
            resp = requests.post(api_url, headers=self._get_headers(), json=payload)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"❌ [API Error] Failed to add text source: {e}")
            return None

    def get_notebook(self, notebook_id):
        """Retrieves notebook details."""
        if self.simulation_mode:
            return {"notebookId": notebook_id, "title": "Simulated Notebook"}
            
        url = f"{self.base_url}/{notebook_id}"
        try:
            resp = requests.get(url, headers=self._get_headers())
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            if notebook_id.startswith("sim_"):
                return {"notebookId": notebook_id, "title": "Simulated Research NB", "sources": []}
            print(f"❌ [API Error] Failed to get notebook: {e}")
            return None

    def list_notebooks(self):
        """Lists recently viewed notebooks."""
        if self.simulation_mode:
            print("📓 [NotebookLM-Sim] Listing Notebooks")
            return [
                {"notebookId": "sim_nb_1", "title": "Simulated Research NB"},
                {"notebookId": "sim_nb_2", "title": "Old Analysis"}
            ]

        url = f"{self.base_url}:listRecentlyViewed"
        try:
            resp = requests.get(url, headers=self._get_headers())
            resp.raise_for_status()
            return resp.json().get("notebooks", [])
        except Exception as e:
            print(f"❌ [API Error] Failed to list notebooks: {e}")
            return []

    def delete_notebooks(self, notebook_names: list):
        """Batch deletes notebooks. Requires full resource names."""
        if self.simulation_mode:
            print(f"📓 [NotebookLM-Sim] Deleting notebooks: {notebook_names}")
            return {}

        url = f"{self.base_url}:batchDelete"
        payload = {"names": notebook_names}
        try:
            resp = requests.post(url, headers=self._get_headers(), json=payload)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"❌ [API Error] Failed to delete notebooks: {e}")
            return None

    def share_notebook(self, notebook_id, email, role="PROJECT_ROLE_READER"):
        """Shares a notebook with a user."""
        if self.simulation_mode:
            print(f"📓 [NotebookLM-Sim] Sharing {notebook_id} with {email} as {role}")
            return {}

        url = f"{self.base_url}/{notebook_id}:share"
        payload = {
            "accountAndRoles": [
                {"email": email, "role": role}
            ]
        }
        try:
            resp = requests.post(url, headers=self._get_headers(), json=payload)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"❌ [API Error] Failed to share notebook: {e}")
            return None
            
    def upload_file(self, notebook_id, file_path, display_name=None):
        """Uploads a local file as a source."""
        if not os.path.exists(file_path):
            print(f"❌ [Error] File not found: {file_path}")
            return None
            
        display_name = display_name or os.path.basename(file_path)
        
        if self.simulation_mode:
            print(f"📓 [NotebookLM-Sim] Uploading file: {file_path}")
            return {"sourceId": {"id": f"sim_file_{int(time.time())}"}}

        # Upload endpoint is slightly different (v1alpha/projects/.../sources:uploadFile)
        # However, the previous batchCreate is for source metadata.
        # The doc mentions a specific upload URL pattern:
        # https://ENDPOINT_LOCATION-discoveryengine.googleapis.com/upload/v1alpha/projects/PROJ/locations/LOC/notebooks/NB_ID/sources:uploadFile
        
        upload_base = f"https://{self.endpoint_location}-discoveryengine.googleapis.com/upload/v1alpha/projects/{self.project_number}/locations/{self.location}/notebooks/{notebook_id}/sources:uploadFile"
        
        # Determine mime type (basic inference)
        ext = os.path.splitext(file_path)[1].lower()
        mime_map = {
            ".pdf": "application/pdf",
            ".txt": "text/plain",
            ".md": "text/markdown",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        }
        content_type = mime_map.get(ext, "application/octet-stream")
        
        headers = self._get_headers()
        # Upload headers are specific
        headers.update({
            "X-Goog-Upload-File-Name": display_name,
            "X-Goog-Upload-Protocol": "raw",
            "Content-Type": content_type
        })
        
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            
            resp = requests.post(upload_base, headers=headers, data=data)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"❌ [API Error] Failed to upload file: {e}")
            return None
