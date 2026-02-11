import asyncio
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

# --- CONFIGURATION ---
KBJ2_ROOT = Path(r"f:\kbj2")
QUEUE_FILE = KBJ2_ROOT / "data" / "queue.json"
INTERVAL_HOURS = 5
RETRY_DELAY_MINUTES = 10

class ContinuousDeveloper:
    def __init__(self):
        self.is_running = True
        if sys.platform == 'win32':
            sys.stdout.reconfigure(encoding='utf-8')

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"🤖 [KCD] {timestamp} | {message}")

    def load_queue(self):
        if not QUEUE_FILE.exists():
            return {"tasks": []}
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_queue(self, data):
        with open(QUEUE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    async def run_kbj2_task(self, task_description):
        """Invoke kbj2 main via subprocess for isolation."""
        self.log(f"Executing: {task_description}")
        
        # We use 'python main.py strat "task"' to trigger the 21-agent team
        cmd = [sys.executable, str(KBJ2_ROOT / "main.py"), "strat", task_description]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=str(KBJ2_ROOT),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            self.log("✅ Task completed successfully.")
            return True, stdout.decode(errors='ignore')
        else:
            self.log(f"❌ Task failed with exit code {process.returncode}")
            return False, stderr.decode(errors='ignore')

    async def sync_git(self, message):
        """Commit and push changes to repository."""
        self.log("Syncing changes to Git...")
        try:
            subprocess.run(["git", "add", "."], cwd=str(KBJ2_ROOT), check=True)
            subprocess.run(["git", "commit", "-m", f"🤖 Auto-Dev: {message}"], cwd=str(KBJ2_ROOT), check=True)
            subprocess.run(["git", "push"], cwd=str(KBJ2_ROOT), check=True)
            self.log("🚀 Git Sync Complete.")
        except Exception as e:
            self.log(f"⚠️ Git Sync Failed: {e}")

    async def main_loop(self):
        self.log("Starting KBJ2 Continuous Developer Service (24h)")
        self.log(f"Scan Interval: {INTERVAL_HOURS} hours")
        
        while self.is_running:
            queue = self.load_queue()
            pending_tasks = [t for t in queue["tasks"] if t["status"] == "pending"]
            
            if not pending_tasks:
                self.log("No pending tasks in queue. Sleeping...")
                await asyncio.sleep(600) # Check queue every 10 mins even when sleeping
                continue

            # Pick highest priority task
            next_task = sorted(pending_tasks, key=lambda x: (x["priority"] != "high", x["priority"] != "medium"))[0]
            
            # Start Processing
            next_task["status"] = "running"
            next_task["updated_at"] = datetime.now().isoformat()
            self.save_queue(queue)

            success, output = await self.run_kbj2_task(next_task["description"])
            
            if success:
                next_task["status"] = "completed"
                await self.sync_git(next_task["description"])
            else:
                next_task["status"] = "failed"
            
            next_task["updated_at"] = datetime.now().isoformat()
            self.save_queue(queue)

            self.log(f"Next cycle in {INTERVAL_HOURS} hours...")
            await asyncio.sleep(INTERVAL_HOURS * 3600)

if __name__ == "__main__":
    cd = ContinuousDeveloper()
    asyncio.run(cd.main_loop())
