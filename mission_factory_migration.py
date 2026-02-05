import os
import sys
import glob
import asyncio
import random

# FORCE UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# --------------------------------------------------------------------------
# MISSION: DEEP MIGRATION (FACTORY TEAM / 100 AGENTS)
# --------------------------------------------------------------------------
# GOAL: Eradicate all legacy "Shipbuilding/SDMS" terminology.
# TARGET: Dynamic (Env Variable)

TARGET_DIR = os.getenv("KBJ2_TARGET_DIR", r"F:\aicitybuilders")

LEGACY_MAP = {
    "Shipyard": "Enterprise Hub",
    "Ship": "System",
    "Vessel": "Module",
    "Maritime": "Global",
    "Dock": "Station",
    "Hull": "Core Structure",
    "Drawings": "Blueprints",
    "SDMS": "SEDMS",
    "sdms": "sedms",
    "Kang": "Commander", # Specific user request cleanup if exists
}

async def factory_migration():
    print("🏭 [Factory_Manager] Initializing 100-Agent Production Line...")
    print("⚡ [Power] High-Voltage Line Active.")
    
    html_files = glob.glob(os.path.join(TARGET_DIR, "*.html"))
    total_tasks = len(html_files)
    
    # Divide labor among 100 workers (Simulated)
    # We assign file chunks to workers
    
    tasks = []
    
    for i, file_path in enumerate(html_files):
        worker_id = f"Worker_{random.randint(1, 100):03d}"
        tasks.append(process_file(file_path, worker_id))
        
    results = await asyncio.gather(*tasks)
    
    total_fixes = sum(results)
    
    print(f"\n✅ [Factory_Manager] Migration Complete. Total Fixes: {total_fixes}")
    print("   Factory Line Shutting Down.")

async def process_file(file_path, worker_id):
    filename = os.path.basename(file_path)
    
    if not os.path.exists(file_path):
        return 0
        
    with open(file_path, "r", encoding="utf-8") as r:
        content = r.read()
        
    new_content = content
    fixes = 0
    
    for old, new in LEGACY_MAP.items():
        if old in new_content:
            new_content = new_content.replace(old, new)
            fixes += 1
            
    if fixes > 0:
        with open(file_path, "w", encoding="utf-8") as w:
            w.write(new_content)
        print(f"🔨 [{worker_id}] Refitted '{filename}' ({fixes} legacy items removed).")
        return fixes
    else:
        # random chance to log 'Checked' to avoid spam, but show activity
        if random.random() < 0.1:
            print(f"👀 [{worker_id}] inspected '{filename}' - Clean.")
        return 0

if __name__ == "__main__":
    asyncio.run(factory_migration())
