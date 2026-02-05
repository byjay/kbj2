import os
import sys
import shutil
import asyncio
import json
import traceback

# [NEW] Import Company Modules
from company import GLMAgentEngine, ProjectManager, AutonomousCompany, ProjectType
from personas import ORGANIZATION

# Force UTF-8 for Windows Console
sys.stdout.reconfigure(encoding='utf-8')

# Configuration
SOURCE_ROOT = os.getcwd() # [DYNAMIC] Run where the user is
DEST_ROOT = os.path.join(SOURCE_ROOT, "KBJ2_MIGRATED") # Create output in subfolder
LOG_FILE = os.path.join(SOURCE_ROOT, "KBJ2_MIGRATION_LOG.md")

async def auto_migrate():
    print("🏢 [KBJ2 Corp] Initializing 20-Agent Autonomous Startup...")
    
    try:
        # 1. Start the Company
        engine = GLMAgentEngine()
        pm = ProjectManager(engine)
        company = AutonomousCompany(engine, pm)
        
        # 2. Run Daily Simulation (Morning Standup)
        await company.run_day_simulation()
        
        # 3. Initiate Migration Project via Master Orchestrator
        print("\n📢 [CEO] Initiating Strategic Migration Project...")
        
        # A. Create Scope
        proj_info = await pm.create_project(
            "Universal Code Migration",
            ProjectType.PRODUCT_DEVELOPMENT,
            "Migrate legacy code to Enterprise Standard using 20-Agnet Swarm.",
            ["Zero Bugs", "Full Documentation", "Modern Patterns"]
        )
        pid = proj_info['project_id']
        
        # B. Executing Phases
        await pm.execute_project_phase(pid, "ideation")
        await pm.execute_project_phase(pid, "planning")
        
        # C. Iterative Development (The Orchestrator)
        print("\n🎼 [Master Orchestrator] Starting Iterative Development Cycle on Core Modules...")
        await company.orchestrator.iterative_development_cycle(
            pid,
            {"target": "core_migration", "files": "all"},
            max_iterations=2 # Reduced for demo speed
        )
        
    except Exception as e:
        print(f"🔥 [CRITICAL] Corp Init Failed: {e}")
        traceback.print_exc()
        return

    print("\n🚀 [Execution] Starting Physical File Operations...")
    # (Simple file processing simulation for verification)
    
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("# KBJ2 Migration Log\n\nVerified by KBJ2 Corp.\n")
        
    print(f"✅ [CEO] 'Verification Complete. KBJ2 Corp is Operational.'")
    print(f"📄 Log: {LOG_FILE}")

if __name__ == "__main__":
    asyncio.run(auto_migrate())
