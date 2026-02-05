import os
import sys
import glob

# Ensure output is UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Mission: Full Codebase Audit for Fintech Division
# Commander: KBJ2 Supreme
# Agent: Audit_Swarm_Leader

TARGET_DIR = r"F:\genmini\stock\ISATS_Ferrari"

def scan_file(filepath):
    """Scans a single file for critical keywords and imports."""
    issues = []
    score = 100
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        lines = content.split('\n')
        
    # Check 1: Deep Insight Integration
    if "execute_real_trade.py" in filepath or "us_trading_launcher.py" in filepath:
        if "DeepInsightV2" not in content and "deep_insight_v2" not in content:
            issues.append("❌ [CRITICAL] 'DeepInsightV2' (AI Brain) is NOT connected to this executor.")
            score -= 40
            
    # Check 2: Hardcoded Paths
    if "C:\\Users\\" in content and "genmini" not in content:
        issues.append("⚠️ [WARNING] Potential hardcoded path detected.")
        score -= 5
        
    # Check 3: Safety Mechanisms
    if "execute" in filepath and "mode" not in content:
         issues.append("❌ [CRITICAL] No 'mode' (Virtual/Real) selection detected.")
         score -= 20
         
    return score, issues

def run_audit():
    print("\n" + "="*60)
    print("🕵️ [KBJ2 AUDIT SWARM] FINTECH DIVISION CODE INSPECTION")
    print("="*60)
    print(f"📍 Target HQ: {TARGET_DIR}")
    
    files = glob.glob(os.path.join(TARGET_DIR, "**/*.py"), recursive=True)
    files.extend(glob.glob(os.path.join(TARGET_DIR, "*.py")))
    files = list(set(files)) # Unique
    
    total_score = 0
    file_count = 0
    
    critical_files = [
        "execute_real_trade.py",
        "us_trading_launcher.py",
        "core\\kis_official_api.py",
        "core\\signal_matrix.py",
        "deep_insight_v2.py"
    ]
    
    print("\n[Phase 1] Deep Scanning Critical Infrastructure...")
    
    for f in files:
        fname = os.path.basename(f)
        is_critical = any(c in f for c in critical_files)
        
        if is_critical or "core" in f:
            score, issues = scan_file(f)
            total_score += score
            file_count += 1
            
            status = "✅ PASS"
            if score < 70: status = "❌ FAIL"
            elif score < 90: status = "⚠️ WARN"
            
            print(f"\n📄 {fname} ... {status} (Integrity: {score}%)")
            for issue in issues:
                print(f"   {issue}")

    avg_score = total_score / file_count if file_count > 0 else 0
    print("\n" + "="*60)
    print(f"🏁 [FINAL VERDICT] SYSTEM INTEGRITY: {avg_score:.1f}%")
    
    if avg_score < 80:
        print("\n🚨 [SYSTEM ALERT] CRITICAL DISCONNECTS FOUND.")
        print("   The 'DeepInsightV2' AI Brain is isolated from the Execution Hands.")
        print("   Immediate Integration is required for 'Full Mobilization'.")
    else:
        print("\n✅ System is fully integrated.")

if __name__ == "__main__":
    run_audit()
