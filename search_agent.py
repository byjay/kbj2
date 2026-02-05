import os
import json
import glob
import time

class KBJ2SearchAgent:
    def __init__(self):
        self.memory = []
        self.data_dir = r"F:\kbj2\data"
        
    def train(self):
        print(f"🧠 [Training] Ingesting knowledge from {self.data_dir}...")
        jsonl_files = glob.glob(os.path.join(self.data_dir, "*.jsonl"))
        
        count = 0
        for filepath in jsonl_files:
            print(f"  - Loading {os.path.basename(filepath)}...")
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            self.memory.append(json.loads(line))
                            count += 1
            except Exception as e:
                print(f"  [Error] Failed to load {filepath}: {e}")
                
        print(f"✅ [Training Complete] Absorbed {count} knowledge items.")
        print(f"   [Knowledge Base] Ready to deploy skills.")

    def search_drive(self, drive_path, keyword=None, max_items=50):
        print(f"\n🔍 [Search] Scanning drive: {drive_path}")
        if keyword:
            print(f"   [Target] Keyword: '{keyword}'")
        else:
            print(f"   [Target] General Scan (listing top-level and exploring)")

        found_count = 0
        try:
            # Simple walk
            for root, dirs, files in os.walk(drive_path):
                # Skip system folders
                if "$RECYCLE.BIN" in root or "System Volume Information" in root:
                    continue
                    
                for file in files:
                    if keyword:
                        if keyword.lower() in file.lower():
                            print(f"  Found: {os.path.join(root, file)}")
                            found_count += 1
                    else:
                        # Just list first few files in each dir to show activity
                        if found_count < max_items:
                            print(f"  [Scanned] {os.path.join(root, file)}")
                            found_count += 1
                        elif found_count == max_items:
                            print("  ... (Truncating output for brevity) ...")
                            found_count += 1
                
                if keyword and found_count >= max_items:
                    break
                    
        except Exception as e:
            print(f"❌ [Error] Access denied or error: {e}")

        print(f"\n✅ [Search Complete] Found/Scanned {found_count} items.")

if __name__ == "__main__":
    agent = KBJ2SearchAgent()
    
    # 1. Train
    agent.train()
    
    # 2. Search
    # User said "search F drive". Assuming general scan or asking user.
    # We will do a general scan of F:\ to prove capability.
    agent.search_drive("F:\\", max_items=20)
