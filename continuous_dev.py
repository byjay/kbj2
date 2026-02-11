import asyncio
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

# --- CONFIGURATION ---
# Cloud-compatible: use relative paths based on script location
KBJ2_ROOT = Path(os.path.dirname(os.path.abspath(__file__)))
QUEUE_FILE = KBJ2_ROOT / "data" / "queue.json"
INTERVAL_HOURS = 5
RETRY_DELAY_MINUTES = 10
HEALTH_PORT = int(os.environ.get("PORT", 8080))

class ContinuousDeveloper:
    def __init__(self):
        self.is_running = True
        self.start_time = datetime.now()
        self.tasks_completed = 0
        self.tasks_failed = 0
        self.last_task = "None"
        try:
            if sys.platform == 'win32':
                sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass

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
                await asyncio.sleep(600)
                continue

            next_task = sorted(pending_tasks, key=lambda x: (x["priority"] != "high", x["priority"] != "medium"))[0]
            
            next_task["status"] = "running"
            next_task["updated_at"] = datetime.now().isoformat()
            self.last_task = next_task["description"][:50]
            self.save_queue(queue)

            success, output = await self.run_kbj2_task(next_task["description"])
            
            if success:
                next_task["status"] = "completed"
                self.tasks_completed += 1
                await self.sync_git(next_task["description"])
            else:
                next_task["status"] = "failed"
                self.tasks_failed += 1
            
            next_task["updated_at"] = datetime.now().isoformat()
            self.save_queue(queue)

            self.log(f"Next cycle in {INTERVAL_HOURS} hours...")
            await asyncio.sleep(INTERVAL_HOURS * 3600)

    # --- Health Endpoint for Render Free Tier ---
    async def start_health_server(self):
        """Lightweight HTTP server so Render considers this a live web service."""
        from aiohttp import web
        
        async def health_handler(request):
            uptime = str(datetime.now() - self.start_time)
            return web.json_response({
                "service": "KBJ2 Continuous Developer",
                "status": "running",
                "uptime": uptime,
                "tasks_completed": self.tasks_completed,
                "tasks_failed": self.tasks_failed,
                "last_task": self.last_task
            })

        app = web.Application()
        app.router.add_get("/", health_handler)
        app.router.add_get("/health", health_handler)
        
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", HEALTH_PORT)
        await site.start()
        self.log(f"🌐 Health endpoint active at http://0.0.0.0:{HEALTH_PORT}")

if __name__ == "__main__":
    cd = ContinuousDeveloper()
    
    async def run_all():
        await cd.start_health_server()
        await cd.main_loop()
    
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_all())
