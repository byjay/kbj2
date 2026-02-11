import requests
import argparse
import sys
import json

CLOUD_URL = "https://kbj2-orchestrator.onrender.com"

def send_task(description, priority="medium"):
    url = f"{CLOUD_URL}/admin/task"
    payload = {
        "description": description,
        "priority": priority
    }
    
    print(f"📡 Sending task to Cloud Agent: '{description}'...")
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Task Queued: {data['task']['id']}")
            print(f"   Status: {data['status']}")
        else:
            print(f"❌ Failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"🔥 Connection Error: {e}")

def check_status():
    url = f"{CLOUD_URL}/health"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("\n📊 Cloud Agent Status")
            print(f"   - Uptime: {data['uptime']}")
            print(f"   - Tasks Completed: {data['tasks_completed']}")
            print(f"   - Tasks Failed: {data['tasks_failed']}")
            print(f"   - Last Task: {data['last_task']}")
            print(f"   - Queue Size: {data.get('queue_size', 'N/A')}")
        else:
            print(f"❌ Status Check Failed: {response.status_code}")
    except Exception as e:
        print(f"🔥 Connection Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="KBJ2 Cloud Commander")
    parser.add_argument("task", nargs="?", help="Task description to send")
    parser.add_argument("--priority", default="medium", choices=["low", "medium", "high"], help="Task priority")
    parser.add_argument("--status", action="store_true", help="Check agent status")
    
    args = parser.parse_args()
    
    if args.status:
        check_status()
    elif args.task:
        send_task(args.task, args.priority)
    else:
        check_status()
        print("\nUsage: python kbj2_cloud.py \"Your task here\"")
