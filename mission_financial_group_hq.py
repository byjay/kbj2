import os
import sys
import subprocess
import time
from datetime import datetime

# Set Project Paths for Imports
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__)) # F:\kbj2
STOCK_ROOT = os.path.join(os.path.dirname(PROJECT_ROOT), "genmini", "stock", "ISATS_Ferrari") # F:\genmini\stock\ISATS_Ferrari

sys.path.insert(0, STOCK_ROOT)

try:
    from deep_insight_v2 import DeepInsightV2
    from core.macro_sentinel import MacroSentinel
    from core.grand_fund_system import FundHIVE
except ImportError as e:
    print(f"❌ [HQ CRITICAL] Subsidiary Communication Failed: {e}")
    # Try adding core path
    sys.path.append(os.path.join(STOCK_ROOT, "core"))
    try:
        from grand_fund_system import FundHIVE
    except ImportError:
        print("   Grand Fund Module not found.")
        sys.exit(1)

def print_logo():
    print(r"""
  _______________________   ____________________ 
 /   _____/\_   _____/   | /   _____/\_   _____/ 
 \_____  \  |    __)_    | \_____  \  |    __)_  
 /        \ |        \   | /        \ |        \ 
/_______  //_______  /___|/_______  //_______  / 
        \/         \/             \/         \/  
      [ ISATS FINANCIAL GROUP HOLDINGS ]
    """)

def run_group_operations(mode="virtual", market="generic"):
    print_logo()
    print(f"🏢 [GROUP HQ] Initiating Operations (Mode: {mode.upper()} | Market: {market.upper()})\n")
    
    # Phase 1: Research Center (The Grand Hive)
    print("="*60)
    print("📡 [PHASE 1] ISATS INTELLIGENCE BUREAU (100-Agent Hive)")
    print("="*60)
    
    hq_hive = FundHIVE(stock_root=STOCK_ROOT)
    top_picks = hq_hive.conduct_morning_meeting()
    
    # Save Top Picks to daily_target_list.csv for Ferrari execution
    if top_picks:
        import pandas as pd
        df = pd.DataFrame(top_picks)
        # Ensure we have required columns for execution engine
        # (ticker, market, score, recommendation, current_price, volume_ratio etc)
        # We fill missing cols with defaults if needed
        # But 'ticker', 'current_price' are key. 'exchange' helps.
        if 'exchange' not in df.columns:
            df['exchange'] = 'NAS' # Fallback
            
        target_csv = os.path.join(STOCK_ROOT, "daily_target_list.csv")
        df.to_csv(target_csv, index=False)
        print(f"✅ [COMMITTEE] Approved {len(top_picks)} targets. Trading Strategy Issued.")
        print(f"   Manifest: {target_csv}")
    else:
        print("⚠️ [COMMITTEE] No suitable targets found. Market conditions unfavorable.")
    
    time.sleep(2)
    
    # Phase 2: Risk Control
    print("\n" + "="*60)
    print("🛡️ [PHASE 2] ISATS RISK CONTROL TOWER")
    print("="*60)
    try:
        sentinel = MacroSentinel()
        defcon = sentinel.check_defcon()
        print(f"   Current DEFCON Level: {defcon}")
        print(f"   Risk Score: {sentinel.risk_score}")
        
        if defcon >= 4:
            print("🚨 [CRITICAL ALERT] DEFCON 4/5 DETECTED. TRADING MAY BE HALTED ORE RESTRICTED.")
        else:
            print("✅ Risk Levels Nominal. Operations Go.")
    except Exception as e:
        print(f"⚠️ [RISK CHECK FAILURE] {e}")

    time.sleep(2)

    # Phase 3: Trading Department (Ferrari)
    print("\n" + "="*60)
    print("🏎️ [PHASE 3] FERRARI TRADING DIVISION (Execution)")
    print("="*60)
    
    exec_script = "us_trading_launcher.py" if market.lower() == "us" else "execute_real_trade.py"
    script_path = os.path.join(STOCK_ROOT, exec_script)
    
    if not os.path.exists(script_path):
        print(f"❌ [HQ ERROR] Execution Engine Not Found: {script_path}")
        return

    cmd = [sys.executable, script_path, "--mode", mode]
    print(f"🚀 Launching Execution Engine: {exec_script} ...")
    
    try:
        # Handoff control to the trading engine
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        print("\n🛑 [HQ] Operation Aborted by User.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Running in Default Virtual Mode (US)...") # Default for demo
        mode = "virtual"
        market = "us"
    else:
        mode = sys.argv[1]
        market = sys.argv[2] if len(sys.argv) > 2 else "generic"
    
    run_group_operations(mode, market)
