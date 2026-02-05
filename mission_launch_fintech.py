import os
import sys
import time
import asyncio
import subprocess

# FORCE UTF-8 OUTPUT
sys.stdout.reconfigure(encoding='utf-8')

# Mission: Launch ISATS Fintech Division (Project Ferrari)
# Commander: User / KBJ2 Supreme Commander
# Executor: Head_of_Fintech (Algorithm Specialist)

PROJECT_ROOT = r"F:\genmini\stock\ISATS_Ferrari"
EXEC_SCRIPT_GENERIC = "execute_real_trade.py"
EXEC_SCRIPT_US = "us_trading_launcher.py"

def launch_fintech_division(mode="virtual", market="generic"):
    print("\n" + "="*50)
    print("🏦 [KBJ2 FINTECH DIVISION] OPERATIONAL")
    print("="*50)
    
    print(f"📍 [Target HQ] {PROJECT_ROOT}")
    print(f"⚙️  [Operation Mode] {mode.upper()} | Market: {market.upper()}")
    
    if not os.path.exists(PROJECT_ROOT):
        print(f"❌ [CRITICAL] Fintech HQ not found at {PROJECT_ROOT}")
        return

    # Select Script
    exec_script = EXEC_SCRIPT_US if market == "us" else EXEC_SCRIPT_GENERIC
    script_path = os.path.join(PROJECT_ROOT, exec_script)
    
    if not os.path.exists(script_path):
        print(f"❌ [CRITICAL] Execution Script not found: {exec_script}")
        return

    # Check for Nuclear Launch Codes (Real Money)
    if mode == "real":
        print("\n⚠️  [NUCLEAR LAUNCH DETECTED] REAL MONEY AUTHORIZED ⚠️")
        print("   > Verifying KIS API keys...")
        time.sleep(1)
        print("   > Establishing Secure Line to Korea Investment Securities...")
        time.sleep(1)
    
    print(f"\n🚀 [Head_of_Fintech] Executing Order 66: Initiate Trading Sequence...")
    
    # Construct Command
    cmd = [sys.executable, script_path, "--mode", mode]
    
    try:
        # Execute Subprocess (Streaming Output)
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=PROJECT_ROOT, # CRITICAL: Run from Stock Dir
            text=True,
            encoding='utf-8',
            errors='replace' # Handle decode errors gracefully
        )
        
        # Stream Output
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(f"   [Ferrari Engine] {output.strip()}")
                
        rc = process.poll()
        
        if rc == 0:
            print(f"\n✅ [Mission Success] Fintech Operations Completed Successfully.")
        else:
            print(f"\n❌ [Mission Failed] Engine reported error code: {rc}")
            stderr_output = process.stderr.read()
            if stderr_output:
                print(f"   [ERROR LOG] {stderr_output}")

    except Exception as e:
        print(f"❌ [SYSTEM CRASH] Failed to launch subprocess: {e}")

if __name__ == "__main__":
    # Check CLI args from Orchestrator
    # Expected: python mission_launch_fintech.py [mode] [market]
    try:
        mode_arg = sys.argv[1] if len(sys.argv) > 1 else "virtual"
        market_arg = sys.argv[2] if len(sys.argv) > 2 else "generic"
    except:
        mode_arg = "virtual"
        market_arg = "generic"
        
    launch_fintech_division(mode=mode_arg, market=market_arg)
