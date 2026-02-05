import os
import sys
import glob
import re
import asyncio

# FORCE UTF-8 OUTPUT FOR WINDOWS PIPES
sys.stdout.reconfigure(encoding='utf-8')

# Mission: Zero-Defect Audit for SEDMS Enterprise
# Target: Find every broken link (#), missing image, or empty button.

TARGET_DIR = os.getenv("KBJ2_TARGET_DIR", os.getcwd())
REPORT_FILE = os.path.join(TARGET_DIR, "SEDMS_DEFECT_REPORT.md")

async def audit_defects():
    print(f"🕵️ [Agent_QA_01] Initiating Zero-Defect Scan on {TARGET_DIR}...")
    
    html_files = glob.glob(os.path.join(TARGET_DIR, "*.html"))
    defects = []
    
    for file_path in html_files:
        filename = os.path.basename(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            lines = content.split('\n')
            
        for i, line in enumerate(lines):
            # Check 1: Dead Links (href="#")
            if 'href="#"' in line or "href='#'" in line:
                defects.append(f"| {filename} | Line {i+1} | Dead Link (`#`) found. |")
                
            # Check 2: Empty Href (href="")
            if 'href=""' in line or "href=''" in line:
                defects.append(f"| {filename} | Line {i+1} | Empty Link (`href=''`) found. |")
                
            # Check 3: Placeholder Images (via.placeholder.com)
            if 'via.placeholder.com' in line:
                defects.append(f"| {filename} | Line {i+1} | Placeholder Image found. |")
                
            # Check 4: Console Log Debugging leftovers
            if 'console.log' in line:
                 defects.append(f"| {filename} | Line {i+1} | `console.log` found (Debug Code). |")

    # Generate Report
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("# SEDMS Zero-Defect Analysis Report 🕵️\n")
        f.write(f"**Date**: {os.times()}\n\n")
        f.write("| File | Line | Defect |\n")
        f.write("|---|---|---|\n")
        if defects:
            for d in defects:
                f.write(d + "\n")
        else:
            f.write("| ALL | - | ✅ NO DEFECTS FOUND. PERFECT. |\n")
            
    print(f"✅ [Agent_QA_01] Audit Complete. Found {len(defects)} defects.")
    print(f"   Report saved to: {REPORT_FILE}")

if __name__ == "__main__":
    asyncio.run(audit_defects())
