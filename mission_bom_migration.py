import os
import shutil
import glob

# KBJ2 BOM MIGRATION AGENT
# Mission: Clone '!!bom' Dashboard to SEDMS Public Assets

SOURCE_DIR = r"F:\!!!진행프로젝트\유일\LOADOUT-BEAM_최종파일\!!bom"
TARGET_BASE = os.getenv("KBJ2_TARGET_DIR", os.getcwd())
DEST_DIR = os.path.join(TARGET_BASE, "public", "legacy_bom_dashboard")

def migrate_assets():
    print(f"📦 [BOM Migration] Source: {SOURCE_DIR}")
    print(f"🎯 [BOM Migration] Dest:   {DEST_DIR}")
    
    if not os.path.exists(SOURCE_DIR):
        print("❌ Source directory not found!")
        return

    # Create Destination
    if os.path.exists(DEST_DIR):
        shutil.rmtree(DEST_DIR)
    os.makedirs(DEST_DIR)
    
    # 1. Copy Critical Code Files
    code_files = ["index.html", "drawing_functions.js", "drawing_list.js", "all_data.js", "styles.css"]
    copied_count = 0
    
    for fname in code_files:
        src_path = os.path.join(SOURCE_DIR, fname)
        if os.path.exists(src_path):
            shutil.copy2(src_path, os.path.join(DEST_DIR, fname))
            print(f"   - Copied Code: {fname}")
            copied_count += 1
            
    # 2. Copy Latest Data Files (Excel)
    # We copy the LATEST weld_export and Drawing_Status
    weld_files = glob.glob(os.path.join(SOURCE_DIR, "weld_export_*.xlsx"))
    if weld_files:
        latest_weld = max(weld_files, key=os.path.getmtime)
        shutil.copy2(latest_weld, os.path.join(DEST_DIR, "weld_data.xlsx"))
        print(f"   - Copied Data: {os.path.basename(latest_weld)} -> weld_data.xlsx")
        copied_count += 1
        
    drawing_files = glob.glob(os.path.join(SOURCE_DIR, "A3_Drawing_Status_*.xlsx"))
    if drawing_files:
        latest_drawing = max(drawing_files, key=os.path.getmtime)
        shutil.copy2(latest_drawing, os.path.join(DEST_DIR, "drawing_status.xlsx"))
        print(f"   - Copied Data: {os.path.basename(latest_drawing)} -> drawing_status.xlsx")
        copied_count += 1

    # 3. Copy Python Scripts (for reference/future backend use)
    py_files = glob.glob(os.path.join(SOURCE_DIR, "*.py"))
    script_dir = os.path.join(DEST_DIR, "scripts")
    os.makedirs(script_dir, exist_ok=True)
    for py in py_files:
        shutil.copy2(py, script_dir)
        
    print(f"✅ Migration Complete. {copied_count} assets transferred.")
    print(f"👉 Access via: /legacy_bom_dashboard/index.html")

if __name__ == "__main__":
    migrate_assets()
