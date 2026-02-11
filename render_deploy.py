"""
Render Deployment Script - Free Tier
Creates services on Render using the free instance plan.
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

def create_web_service(name, repo_url, branch="main", dockerfile_path="./Dockerfile"):
    """Create a Web Service on Render Free Tier"""
    url = "https://api.render.com/v1/services"
    payload = {
        "type": "web_service",
        "name": name,
        "ownerId": OWNER_ID,
        "repo": repo_url,
        "branch": branch,
        "autoDeploy": "yes",
        "serviceDetails": {
            "env": "docker",
            "dockerfilePath": dockerfile_path,
            "plan": "free",
            "region": "oregon",
            "numInstances": 1
        }
    }
    print(f"📡 Creating Web Service '{name}'...")
    response = requests.post(url, json=payload, headers=HEADERS)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    return response

def create_background_worker(name, repo_url, branch="main", dockerfile_path="./Dockerfile"):
    """Create a Background Worker on Render Free Tier"""
    url = "https://api.render.com/v1/services"
    payload = {
        "type": "background_worker",
        "name": name,
        "ownerId": OWNER_ID,
        "repo": repo_url,
        "branch": branch,
        "autoDeploy": "yes",
        "serviceDetails": {
            "env": "docker",
            "dockerfilePath": dockerfile_path,
            "plan": "starter",
            "region": "oregon",
            "numInstances": 1
        }
    }
    print(f"📡 Creating Background Worker '{name}'...")
    response = requests.post(url, json=payload, headers=HEADERS)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    return response

def list_services():
    url = "https://api.render.com/v1/services"
    response = requests.get(url, headers=HEADERS)
    services = response.json()
    print(f"\n📋 Current Services ({len(services)}):")
    for s in services:
        svc = s['service']
        print(f"   - {svc['name']} ({svc['type']}) | ID: {svc['id']} | Status: {svc.get('suspended', 'active')}")
    return services

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 ISATS RENDER DEPLOYMENT")
    print("=" * 60)
    
    # Step 1: Create Stock Dashboard (Web Service - Free)
    r1 = create_web_service(
        "isats-stock-dashboard",
        "https://github.com/byjay/stock",
        dockerfile_path="./Dockerfile"
    )
    
    # Step 2: Create KBJ2 Orchestrator (Background Worker)
    r2 = create_background_worker(
        "kbj2-orchestrator",
        "https://github.com/byjay/kbj2",
        dockerfile_path="./Dockerfile"
    )
    
    # Step 3: List all services
    list_services()
