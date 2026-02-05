
import win32com.client
import os
import time
import sys

# Parameters
TARGET_FILE = r"f:\!!!진행프로젝트\HS\참치\HK2401 Cable List-포설실적용_260203_TEST.xlsm"
MACRO_NAME = "UpdateCableList_Delta"

def log(msg):
    print(f"[KBJ-Trigger] {msg}")

def trigger_macro():
    if not os.path.exists(TARGET_FILE):
        log(f"❌ Error: File not found at {TARGET_FILE}")
        return

    try:
        log("1. Connecting to Excel...")
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = True # Make it visible so user can see the Dialog
        
        log(f"2. Opening Workbook: {os.path.basename(TARGET_FILE)}")
        wb = excel.Workbooks.Open(TARGET_FILE)
        
        log(f"3. Triggering Macro: '{MACRO_NAME}'")
        log("   📢 The File Selection Dialog should appear on your screen now.")
        
        # This will block until the user closes the dialog/macro finishes
        excel.Application.Run(MACRO_NAME)
        
        log("✅ Macro execution completed.")
        # We leave it open for the user to inspect
        
    except Exception as e:
        log(f"❌ Error triggering macro: {e}")

if __name__ == "__main__":
    trigger_macro()
