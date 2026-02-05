import os
import requests
import json

# Force UTF-8
import sys
sys.stdout.reconfigure(encoding='utf-8')

API_URL = "https://api.z.ai/api/coding/paas/v4/chat/completions"
ENV_KEY = os.environ.get("ZAI_API_KEY", "")

if not ENV_KEY:
    print("❌ ZAI_API_KEY is missing.")
    sys.exit(1)

keys = [k.strip() for k in ENV_KEY.split(",") if k.strip()]
print(f"🔑 Found {len(keys)} API keys.")

payload = {
    "model": "GLM-4.7",
    "messages": [{"role": "user", "content": "Hello"}],
    "temperature": 0.1
}

for i, key in enumerate(keys):
    masked = key[:4] + "..." + key[-4:]
    print(f"\n📡 Testing Key #{i+1} ({masked})...")
    
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Success!")
        else:
            print(f"   ❌ Failed: {response.text}")
            
    except Exception as e:
        print(f"   🔥 Connection Error: {e}")
