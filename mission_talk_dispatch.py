import os
import sys
import time
import logging
from datetime import datetime

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")
logger = logging.getLogger("TALK_DISPATCH")

class TalkDispatcher:
    def __init__(self):
        self.journal_path = "NIGHT_OPS_JOURNAL.md"
        self.last_pos = 0
        self.talk_active = False
        
    def initialize(self):
        print("\n📲 [TALK DISPATCH] Initializing Mobile Alert System...")
        # Check Journal
        if not os.path.exists(self.journal_path):
            print(f"⚠️ Journal not found at {self.journal_path}. Waiting for Night Ops...")
            # Create dummy if needed or wait
            with open(self.journal_path, 'w') as f:
                f.write("# NIGHT OPS LOG\n")
        
        # Seek to end
        self.last_pos = os.path.getsize(self.journal_path)
        print("✅ Connected to Night Ops Frequency.")
        print("✅ Talk Gateway Ready (Simulation Mode).")
        return True

    def send_to_talk(self, message):
        """
        Simulates sending a message to KakaoTalk.
        In a full automation setup, this would use pywinauto/pyautogui.
        """
        timestamp = datetime.now().strftime("%H:%M")
        
        # Formatting for Talk
        formatted_msg = f"""
[ISATS 🚨 BREAKING] {timestamp}
{message}
-------------------
Grand Fund HQ
"""
        print(f"\n📨 [SENDING TO TALK]...")
        time.sleep(0.5)
        print(f"   Success: Message delivered to 'Projects' Chatroom.")
        print(f"   Payload: {message.strip()}")
        
    def monitor_loop(self):
        print("👀 Monitoring Trading Activity...")
        try:
            while True:
                if os.path.exists(self.journal_path):
                    current_size = os.path.getsize(self.journal_path)
                    if current_size > self.last_pos:
                        with open(self.journal_path, 'r', encoding='utf-8') as f:
                            f.seek(self.last_pos)
                            new_lines = f.readlines()
                            self.last_pos = f.tell()
                            
                        for line in new_lines:
                            if "BUY" in line or "SELL" in line or "MISSION" in line:
                                # Clean line
                                clean_msg = line.split("|")[-1].strip()
                                self.send_to_talk(clean_msg)
                                
                time.sleep(2)
        except KeyboardInterrupt:
            print("\n🛑 Dispatch Offline.")

if __name__ == "__main__":
    dispatcher = TalkDispatcher()
    if dispatcher.initialize():
        dispatcher.monitor_loop()
