import os
import requests
import json

# Corrected Z.AI Endpoint
BASE_URL = "https://api.z.ai/api/paas/v4/chat/completions"

KEYS = [
    "384fffa4d8a44ce58ee573be0d49d995.kqLAZNeRmjnUNPJh",
    "9c5b377b9bf945d0a2b00eacdd9904ef.BoRiu74O1h0bV2v6",
    "a9bd9bd3917c4229a49f91747c4cf07e.PQBgL1cU7TqcNaBy"
]

print(f"🔌 Testing Connection to Z.AI (GLM-4.7) with {len(KEYS)} Keys...")

for i, API_KEY in enumerate(KEYS):
    print(f"\n🔑 Trying Key #{i+1}: {API_KEY[:10]}...")
    headers = {
        "Authorization": f"Bearer {API_KEY.split('.')[0]}", 
        "Content-Type": "application/json"
    }

# Payload per User Config (OpenAI Compatible)
payload = {
    "model": "glm-4",
    "messages": [
        {"role": "user", "content": "Hello, are you GLM-4.7?"}
    ],
    "temperature": 0.5,
    "max_tokens": 100
}

try:
    resp = requests.post(BASE_URL, headers=headers, json=payload, timeout=10)
    print(f"📡 Status Code: {resp.status_code}")
    print(f"📩 Response: {resp.text[:500]}")
    
    if resp.status_code == 200:
        print("✅ GLM-4.7 Connection SUCCESS!")
    else:
        print("❌ Connect Failed.")

except Exception as e:
    print(f"❌ Exception: {e}")
