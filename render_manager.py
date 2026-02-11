import requests
import json
import sys

API_KEY = "rnd_0BK7WmLKLgDJLSltwl0Sx8P6dg91"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def list_services():
    url = "https://api.render.com/v1/services"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        services = response.json()
        print(f"✅ Found {len(services)} services.")
        for s in services:
            print(f"- {s['service']['name']} ({s['service']['type']}): {s['service']['id']}")
        return services
    else:
        print(f"❌ Failed to list services: {response.status_code}")
        print(response.text)
        return None

def get_owners():
    url = "https://api.render.com/v1/owners"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        owners = response.json()
        print(f"✅ Found {len(owners)} owners.")
        for o in owners:
            print(f"- {o['owner']['name']} ({o['owner']['type']}): {o['owner']['id']}")
        return owners
    else:
        print(f"❌ Failed to get owners: {response.status_code}")
        print(response.text)
        return None

def create_service(name, service_type, repo_url, owner_id):
    url = "https://api.render.com/v1/services"
    payload = {
        "type": service_type,
        "name": name,
        "repo": repo_url,
        "autoDeploy": "yes",
        "ownerId": owner_id,
        "serviceDetails": {
            "env": "docker"
        }
    }
    response = requests.post(url, json=payload, headers=HEADERS)
    if response.status_code in [201, 200]:
        service = response.json()
        print(f"✅ Service '{name}' created/updated: {service['service']['id']}")
        return service
    else:
        print(f"❌ Failed to create service '{name}': {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    owner_id = "tea-d4p99meuk2gs73d84qk0"
    # Create KBJ2 Background Worker
    create_service("kbj2-orchestrator", "background_worker", "https://github.com/byjay/kbj2", owner_id)
    # Create Stock Web Service
    create_service("isats-stock-dashboard", "web_service", "https://github.com/byjay/stock", owner_id)
    list_services()
