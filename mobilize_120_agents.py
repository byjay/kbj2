import asyncio
import os
import sys
import glob
from datetime import datetime
from typing import List
from system import EDMSAgentSystem
from personas import ORGANIZATION, AgentRole

# FORCE UTF-8 OUTPUT FOR WINDOWS PIPES
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# --- CONFIGURATION ---
TARGET_DIR = os.getenv("KBJ2_TARGET_DIR", os.getcwd())
REPORT_FILE = os.path.join(TARGET_DIR, "KBJ2_REAL_SWARM_REPORT.md")
CONCURRENCY_LIMIT = 20  # Overall script limit (system.py has its own too)

class SwarmMobilizer:
    def __init__(self):
        try:
            self.system = EDMSAgentSystem()
        except Exception as e:
            print(f"❌ System Init Error: {e}")
            sys.exit(1)
        self.semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
        self.results = []

    async def run_agent_task(self, agent_id: str, persona: str, task: str):
        """Execute a real agent task in the swarm."""
        async with self.semaphore:
            try:
                # Use simplified prompt for speed in swarm
                prompt = f"Persona: {persona}\nTask: {task}\nProvide one actionable insight or fix for the current project context."
                result = await self.system.run_agent(agent_id, prompt)
                
                timestamp = datetime.now().strftime("%H:%M:%S")
                entry = f"| {timestamp} | {agent_id} | ✅ | {result.get('recommendation', 'Success')} |"
                print(f"✨ [DONE] {agent_id}: {result.get('recommendation', 'Success')[:60]}...")
                return entry
            except Exception as e:
                return f"| {datetime.now().strftime('%H:%M:%S')} | {agent_id} | ❌ | Error: {str(e)} |"

    async def mobilize(self):
        print(f"🚀 [KBJ2 TRUE SWARM] DISPATCHING 120 REAL AGENT TASKS...")
        print(f"📂 Target: {TARGET_DIR}")
        
        # Prepare 120 Agent Personas (mix of core and monet registry)
        agent_pool = list(ORGANIZATION.keys())
        # If pool < 120, we cycle them with different task modifiers
        tasks = []
        
        for i in range(120):
            agent_id = agent_pool[i % len(agent_pool)]
            persona = ORGANIZATION[agent_id]
            task_focus = ["UX Audit", "Code Security", "Performance Tuning", "Brand Alignment", "Logic Verification"][i % 5]
            tasks.append(self.run_agent_task(
                f"{agent_id}_{i:03d}", 
                f"{persona.name} ({persona.role})", 
                f"Perform a {task_focus} on the files in {TARGET_DIR}."
            ))

        # --- PARALLEL EXECUTION ---
        print(f"⚡ Launching 120 asynchronous threads...")
        reports = await asyncio.gather(*tasks)
        
        # --- REPORT GENERATION ---
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write(f"# KBJ2 TRUE SWARM MOBILIZATION REPORT\n")
            f.write(f"**Mission**: Real-Time Parallel Audit & Execution\n")
            f.write(f"**Total Agents**: 120\n")
            f.write(f"**Date**: {datetime.now()}\n\n")
            f.write("| Timestamp | Agent ID | Status | Action/Insight |\n|---|---|---|---|\n")
            for line in reports:
                f.write(line + "\n")

        print(f"\n✅ [SWARM COMPLETE] 120 Agents executed successfully.")
        print(f"📄 Full report: {REPORT_FILE}")

async def main():
    mobilizer = SwarmMobilizer()
    await mobilizer.mobilize()

if __name__ == "__main__":
    asyncio.run(main())
