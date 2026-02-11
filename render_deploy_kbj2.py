"""
Render Deploy KBJ2 as Web Service (Free Tier Workaround)
Background workers require paid plan, so we deploy KBJ2 as a web service 
that runs a lightweight HTTP health endpoint alongside the continuous dev loop.
"""
import requests
import json

API_KEY = "rnd_0BK7WmLKLgDJLSltwl0Sx8P6dg91"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}
OWNER_ID = "tea-d4p99meuk2gs73d84qk0"

url = "https://api.render.com/v1/services"
payload = {
    "type": "web_service",
    "name": "kbj2-orchestrator",
    "ownerId": OWNER_ID,
    "repo": "https://github.com/byjay/kbj2",
    "branch": "main",
    "autoDeploy": "yes",
    "serviceDetails": {
        "env": "docker",
        "dockerfilePath": "./Dockerfile",
        "plan": "free",
        "region": "oregon",
        "numInstances": 1
    }
}
print("📡 Creating KBJ2 Orchestrator as Web Service (Free Tier)...")
response = requests.post(url, json=payload, headers=HEADERS)
print(f"   Status: {response.status_code}")
print(json.dumps(response.json(), indent=2))
