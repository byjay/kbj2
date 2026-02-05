import os
import sys
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

# Path Setup
ferrari_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "genmini", "stock", "ISATS_Ferrari"))
sys.path.append(ferrari_path)

try:
    from core.kis_official_api import KISUnifiedClient
except ImportError:
    sys.path.append(os.path.join(ferrari_path, "core"))
    from kis_official_api import KISUnifiedClient

def audit_real_account():
    print("🔍 [AUDIT] Connecting to KIS REAL SERVER...")
    # Mode="real" connects to actual trading server
    client = KISUnifiedClient(mode="real")
    
    if not client.auth.get_access_token():
        print("❌ Real Auth Failed. Check APP_KEY/SECRET for Real Mode.")
        return
        
    print("✅ Real Auth Success.")
    
    # Check Balance (PSBL_ORDER_AMT)
    acc = client.auth.account_no
    print(f"💳 Account: {acc}")
    
    # Get Balance
    # Note: KIS API balance structure overrides
    balance_info = client.overseas_stock.get_balance()
    
    if balance_info:
        # Looking for 'dnca_tot_amt' (Deposit) or similar
        # For simplified unified client, we inspect the raw return dict
        # Typically 'output2' contains summary in many KIS TRs
        print(f"💰 Balance Data: {balance_info}")
        
    else:
        print("⚠️ Failed to retrieve balance.")

if __name__ == "__main__":
    audit_real_account()
