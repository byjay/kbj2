import asyncio
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict

@dataclass
class AgentTask:
    id: str
    priority: int  # 0 = High, 10 = Low
    func: Callable[..., Any]
    args: tuple
    kwargs: Dict[str, Any]
    future: asyncio.Future
    
    def __lt__(self, other):
        return self.priority < other.priority

class CentralScheduler:
    """
    Manages global API concurrency to prevent 429 errors.
    Acts as the 'Traffic Controller' for the massive multi-agent system.
    """
    def __init__(self, requests_per_minute: int = 20):
        self.queue = asyncio.PriorityQueue()
        self.workers = []
        self.is_running = False
        # Calculate delay between requests to stay safe
        # e.g., 20 RPM = 1 request every 3 seconds
        self.safe_delay = 60.0 / requests_per_minute
        self.last_request_time = 0.0

    async def start(self):
        self.is_running = True
        # We start a single worker that pulls from priority queue
        # This guarantees strict sequential issuance if needed, or we can scale workers
        self.workers.append(asyncio.create_task(self._worker_loop()))
        print(f"⚡ [Scheduler] Started. Rate Limit: ~{self.safe_delay:.2f}s delay.")

    async def stop(self):
        self.is_running = False
        await self.queue.join()
        for w in self.workers:
            w.cancel()

    async def submit_task(self, func: Callable, *args, priority: int = 5, **kwargs) -> Any:
        """Submits a task to the queue and returns the result."""
        future = asyncio.get_event_loop().create_future()
        task = AgentTask(
            id=f"{time.time()}",
            priority=priority,
            func=func,
            args=args,
            kwargs=kwargs,
            future=future
        )
        # PriorityQueue uses tuple comparison, so (priority, timestamp) works naturally
        await self.queue.put((priority, time.time(), task))
        return await future

    async def _worker_loop(self):
        while self.is_running:
            try:
                # Get task
                priority, timestamp, task = await self.queue.get()
                
                # Rate Limiting Logic
                now = time.time()
                elapsed = now - self.last_request_time
                if elapsed < self.safe_delay:
                    wait_time = self.safe_delay - elapsed
                    # print(f"⏳ [Scheduler] Throttling for {wait_time:.2f}s...")
                    await asyncio.sleep(wait_time)
                
                # Execute
                try:
                    result = await task.func(*task.args, **task.kwargs)
                    task.future.set_result(result)
                    self.last_request_time = time.time()
                except Exception as e:
                    task.future.set_exception(e)
                finally:
                    self.queue.task_done()
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"❌ [Scheduler] Worker Error: {e}")

# Global instance
SCHEDULER = CentralScheduler(requests_per_minute=25) # Slightly aggressive but safe
