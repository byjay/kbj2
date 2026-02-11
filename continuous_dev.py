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

    async def run_kbj2_task(self, task):
        """Invoke kbj2 main via subprocess. Task can be string or dict."""
        
        if isinstance(task, dict) and task.get("type") == "monitor":
            self.log(f"🕵️‍♂️ Launching Real-time Stock Monitor...")
            cmd = [sys.executable, str(KBJ2_ROOT / "main.py"), "monitor", "--duration", "25"]
        else:
            description = task["description"] if isinstance(task, dict) else task
            self.log(f"Executing: {description}")
            cmd = [sys.executable, str(KBJ2_ROOT / "main.py"), "strat", description]
        
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
            # Ensure data directory is tracked
            subprocess.run(["git", "add", "data/"], cwd=str(KBJ2_ROOT), check=False)
            subprocess.run(["git", "add", "."], cwd=str(KBJ2_ROOT), check=True)
            subprocess.run(["git", "commit", "-m", f"🤖 Auto-Dev: {message}"], cwd=str(KBJ2_ROOT), check=True)
            subprocess.run(["git", "push"], cwd=str(KBJ2_ROOT), check=True)
            self.log("🚀 Git Sync Complete.")
        except Exception as e:
            self.log(f"⚠️ Git Sync Failed: {e}")

    async def main_loop(self):
        self.log("Starting KBJ2 Continuous Developer Service (24h)")
        
        while self.is_running:
            # --- Night Shift Logic (US Market Hours: 22:00 - 06:00 KST) ---
            now_utc = datetime.utcnow()
            hour_utc = now_utc.hour
            is_night_shift = 13 <= hour_utc < 21
            
            queue = self.load_queue()
            pending_tasks = [t for t in queue["tasks"] if t["status"] == "pending"]
            
            # [Night Shift] Auto-Generate Real-time Monitor Task
            if is_night_shift and not pending_tasks:
                self.log("🌙 Night Shift Active: Launching Real-time US Stock Monitor...")
                us_task = {
                    "id": f"monitor_{int(datetime.now().timestamp())}",
                    "type": "monitor", # Special type for logic routing
                    "description": "Real-time US Market Monitoring & Trading Analysis",
                    "status": "pending",
                    "priority": "high",
                    "created_at": datetime.now().isoformat()
                }
                queue["tasks"].append(us_task)
                pending_tasks.append(us_task)
                self.save_queue(queue)
                current_interval = 25 * 60 # 25 min duration + sync time
            else:
                current_interval = INTERVAL_HOURS * 3600 # 5 hours normally

            if not pending_tasks:
                self.log(f"No pending tasks. Sleeping for {current_interval/3600:.1f} hours...")
                # Still check every 10 mins for remote commands
                await asyncio.sleep(600)
                continue

            # Pick highest priority task
            next_task = sorted(pending_tasks, key=lambda x: (x["priority"] != "high", x["priority"] != "medium"))[0]
            
            # Start Processing
            next_task["status"] = "running"
            next_task["updated_at"] = datetime.now().isoformat()
            self.last_task = next_task["description"][:50]
            self.save_queue(queue)

            # Pass the entire task object to support 'type' checking
            success, output = await self.run_kbj2_task(next_task)
            
            if success:
                next_task["status"] = "completed"
                self.tasks_completed += 1
                await self.sync_git(next_task["description"])
            else:
                next_task["status"] = "failed"
                self.tasks_failed += 1
            
            next_task["updated_at"] = datetime.now().isoformat()
            self.save_queue(queue)

            # Determine sleep time based on shift
            # If night shift, sleep just a bit to allow sync, then loop again immediately
            sleep_time = 60 if is_night_shift else current_interval
            
            if is_night_shift:
               self.log(f"🌙 Night Shift: Recycling in 1 minute...")
            else:
               self.log(f"Next cycle in {sleep_time/3600:.1f} hours...")
               
            await asyncio.sleep(sleep_time)

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
                "last_task": self.last_task,
                "queue_size": len(self.load_queue()["tasks"])
            })

        async def add_task_handler(request):
            try:
                data = await request.json()
                description = data.get("description")
                priority = data.get("priority", "medium")
                
                if not description:
                    return web.json_response({"error": "Description required"}, status=400)
                
                new_task = {
                    "id": f"task_{int(datetime.now().timestamp())}",
                    "description": description,
                    "status": "pending",
                    "priority": priority,
                    "created_at": datetime.now().isoformat()
                }
                
                queue = self.load_queue()
                queue["tasks"].append(new_task)
                self.save_queue(queue)
                
                self.log(f"📨 Remote Task Received: {description}")
                return web.json_response({"status": "queued", "task": new_task})
            except Exception as e:
                return web.json_response({"error": str(e)}, status=500)

        app = web.Application()
        app.router.add_get("/", health_handler)
        app.router.add_get("/health", health_handler)
        app.router.add_post("/admin/task", add_task_handler) # Remote Command Endpoint
        
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", HEALTH_PORT)
        await site.start()
        self.log(f"🌐 Health endpoint active at http://0.0.0.0:{HEALTH_PORT}")

    # --- Keep-Alive Mechanism ---
    async def keep_alive(self):
        """Ping the Stock Dashboard every 14 minutes to prevent sleep."""
        import aiohttp
        url = "https://isats-stock-dashboard.onrender.com"
        self.log(f"⏰ Keep-Alive System Activated: Pinging {url} every 14 mins")
        
        async with aiohttp.ClientSession() as session:
            while self.is_running:
                try:
                    async with session.get(url) as resp:
                        status = resp.status
                        self.log(f"💓 Ping sent to Stock Dashboard. Status: {status}")
                except Exception as e:
                    self.log(f"⚠️ Keep-Alive Ping Failed: {e}")
                
                await asyncio.sleep(14 * 60) # 14 minutes

if __name__ == "__main__":
    cd = ContinuousDeveloper()
    
    async def run_all():
        await asyncio.gather(
            cd.start_health_server(),
            cd.main_loop(),
            cd.keep_alive()
        )
    
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_all())
