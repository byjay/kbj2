import sys
import os
import logging

# Path setup
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# F:\kbj2 -> F:\genmini\stock\ISATS_Ferrari
STOCK_ROOT = os.path.join(os.path.dirname(PROJECT_ROOT), "genmini", "stock", "ISATS_Ferrari")
sys.path.insert(0, STOCK_ROOT)

try:
    from core.kis_official_api import KISUnifiedClient
except ImportError:
    # Fallback: Maybe core is not a package? Try adding core to path
    sys.path.append(os.path.join(STOCK_ROOT, "core"))
    from kis_official_api import KISUnifiedClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DEBUGGER")

def test_price():
    print("🔎 [DEBUG] Testing US Stock Price Fetch (Virtual Mode)...")
    
    # Initialize Client
    try:
        client = KISUnifiedClient(mode="virtual")
    except Exception as e:
        print(f"❌ Client Init Failed: {e}")
        return

    if not client.auth.get_access_token():
        print("❌ Auth Failed")
        return

    targets = ["AAPL", "TSLA", "NVDA", "SPY"]
    
    for t in targets:
        print(f"\n📡 Fetching {t}...")
        
        # Method: get_price(ticker, market="US")
        try:
            price_info = client.get_price(t, market="US")
            print(f"   [Result Raw] {price_info}")
            
            p = float(price_info.get('price', 0))
            if p > 0:
                print(f"   ✅ Price: ${p}")
            else:
                print(f"   ⚠️ Price is ZERO or Missing")
                
        except Exception as e:
            print(f"   ❌ Fetch Error: {e}")

if __name__ == "__main__":
    test_price()
