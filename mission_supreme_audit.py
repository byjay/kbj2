import os
import glob
import re

TARGET_DIR = os.getenv("KBJ2_TARGET_DIR", os.getcwd())
REPORT_FILE = os.path.join(TARGET_DIR, "kbj2_reports", "KBJ2_SUPREME_AUDIT_REPORT.md")

def check_jsx_balance(content):
    # Very basic heuristic for unclosed tags
    opens = len(re.findall(r'<div', content))
    closes = len(re.findall(r'</div>', content))
    return opens - closes

def audit_tsx():
    print("🦅 [Supreme Audit] Scanning SEDMS React Codebase...")
    
    files = glob.glob(os.path.join(TARGET_DIR, "src", "**", "*.tsx"), recursive=True)
    report = []
    report.append("# SEDMS Supreme Audit Report")
    report.append(f"**Target**: {TARGET_DIR}")
    report.append(f"**Files Scanned**: {len(files)}\n")
    
    issues_found = 0
    
    for fpath in files:
        fname = os.path.basename(fpath)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Check 1: Div Balance
            balance = check_jsx_balance(content)
            if balance != 0:
                report.append(f"- ⚠️ **{fname}**: Div Mismatch (Balance: {balance}). Potential Syntax Error.")
                issues_found += 1
                
            # Check 2: Header Duplication
            if content.count("import React") > 1:
                report.append(f"- ⚠️ **{fname}**: Duplicate Imports detected.")
                issues_found += 1
                
            # Check 3: Critical TODOs
            todos = len(re.findall(r'TODO:', content))
            if todos > 0:
                report.append(f"- ℹ️ **{fname}**: {todos} Pending Tasks.")
                
        except Exception as e:
            report.append(f"- ❌ **{fname}**: Read Error ({str(e)})")
            
    if issues_found == 0:
        report.append("\n**Result**: No Critical Syntax Defects Found.")
    else:
        report.append(f"\n**Result**: {issues_found} Critical Issues Detected.")
        
    # Write Report
    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(report))
        
    print(f"✅ Audit Complete. Report: {REPORT_FILE}")

if __name__ == "__main__":
    audit_tsx()
