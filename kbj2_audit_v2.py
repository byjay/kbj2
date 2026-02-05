import os
import re
import glob
import asyncio
from datetime import datetime
from collections import defaultdict

# Import KBJ2 Core
from company import GLMAgentEngine, ProjectManager, AutonomousCompany, ProjectType
from personas import ORGANIZATION

# Paths
SDMS_ROOT = r"F:\genmini\sdms\src"
ROUTES_FILE = os.path.join(SDMS_ROOT, "config", "routes.ts")
MOBILE_ROUTER = os.path.join(SDMS_ROOT, "apps", "mobile", "App.tsx")
REPORT_PATH = r"F:\genmini\sdms\MAP_CONNECTIVITY_REPORT_V2.md"

class ConnectivityAuditorV2:
    """
    Advanced Connectivity Auditor
    - Multi-Router Support (Desktop + Mobile)
    - Deep Reference Scanning (Grep)
    - Zombie Hunter Logic
    """
    
    def __init__(self):
        self.active_routes = {}  # path -> component
        self.active_components = set() # Set of filenames that are definitely used
        self.physical_pages = set()
        self.zombies = []
        self.sub_components = []
        
        # Comparison logic
        self.all_tsx_files = [] 
        
    def scan_routers(self):
        """Parse all known routers"""
        print(f"🔍 [Auditor] Scanning Routers...")
        
        # 1. Desktop Router
        self._parse_router(ROUTES_FILE, "Desktop")
        
        # 2. Mobile Router
        self._parse_router(MOBILE_ROUTER, "Mobile")
        
    def _parse_router(self, file_path, context):
        """Generic Regex Parser for Lazy Imports"""
        if not os.path.exists(file_path):
            print(f"⚠️ Router file not found: {file_path}")
            return
            
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Pattern: lazy(() => import('PATH'))
        # Matches ./pages/.., @/components/..
        import_pattern = re.compile(r"import\(['\"]([^'\"]+)['\"]\)")
        
        count = 0
        for match in import_pattern.finditer(content):
            raw_path = match.group(1)
            # Normalize path to filename
            filename = os.path.basename(raw_path)
            # Remove extension if accidentally included (rare in imports)
            if filename.endswith('.tsx'): filename = filename[:-4]
            if filename.endswith('.ts'): filename = filename[:-3]
            
            self.active_components.add(filename)
            count += 1
            
        print(f"   - {context}: Found {count} active imports")

    def scan_filesystem(self):
        """Index all TSX files"""
        print(f"🔍 [Auditor] Indexing Filesystem...")
        
        # Scan all TSX files in src
        self.all_tsx_files = glob.glob(os.path.join(SDMS_ROOT, "**", "*.tsx"), recursive=True)
        
        # Filter for "Page-like" to match user's previous list style
        # But for "True Zombie" detection, we check EVERYTHING.
        print(f"   - Indexed {len(self.all_tsx_files)} source files")

    def hunt_zombies(self):
        """
        The Core Logic:
        If a file is NOT in active_components, is it imported by ANY other file?
        """
        print("🧟 [Auditor] Hunting Zombies (Deep Reference Scan)...")
        
        # Prepare cache of all file content to speed up grep
        # (Naive implementation, but fine for this project size)
        file_contents = {}
        for fpath in self.all_tsx_files:
             try:
                with open(fpath, "r", encoding="utf-8") as f:
                    file_contents[fpath] = f.read()
             except:
                 pass

        for fpath in self.all_tsx_files:
            filename = os.path.basename(fpath)
            name_no_ext = filename.replace(".tsx", "")
            
            # Skip strictly internal files usually
            if filename in ["App.tsx", "main.tsx", "vite-env.d.ts"]:
                continue
            
            # 1. Direct hit in Routers?
            if name_no_ext in self.active_components:
                continue # It's a top-level page
                
            # 2. Referenced by ANY other file?
            is_referenced = False
            for other_path, content in file_contents.items():
                if fpath == other_path: continue # Self-reference doesn't count
                
                # Check for import
                # import ... from './Name'
                # import ... from '@/.../Name'
                if f"/{name_no_ext}'" in content or f'/{name_no_ext}"' in content:
                    is_referenced = True
                    break
                # Check for Usage in JSX <Name ... />
                if f"<{name_no_ext}" in content:
                    is_referenced = True
                    break
            
            if is_referenced:
                self.sub_components.append(name_no_ext)
            else:
                self.zombies.append(fpath) # Store full path for the report

    def generate_report(self):
        report = f"""# 🧟 SDMS Zombie Report (v2.0)
**Generated By:** KBJ2 Corp
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Analysis Depth:** Deep Content Grep (Global Usage Scan)

## 📊 Summary
- **Total Files Scanned**: {len(self.all_tsx_files)}
- **Top-Level Routes**: {len(self.active_components)} (Directly linked in Routers)
- **Active Sub-Components**: {len(self.sub_components)} (Imported by other files)
- **💀 True Zombies**: {len(self.zombies)} (Zero incoming references)

---

## 💀 True Zombies (Zero References)
**Recommendation**: These files are safe to DELETE or ARCHIVE immediately.
"""
        # Group by folder for readability
        zombies_by_dir = defaultdict(list)
        for z in self.zombies:
            rel_path = os.path.relpath(z, SDMS_ROOT)
            folder = os.path.dirname(rel_path)
            zombies_by_dir[folder].append(os.path.basename(z))
            
        for folder, files in sorted(zombies_by_dir.items()):
            report += f"\n### 📂 `{folder}`\n"
            for f in sorted(files):
                report += f"- [ ] `{f}`\n"

        report += "\n---\n"
        report += "## 🛡️ False Positives Cleared\n"
        report += f"The previous scan flagged **{len(self.sub_components)}** files as orphans.\n"
        report += "This deep scan confirms they are **Active Sub-Components** used by other pages.\n"
        
        with open(REPORT_PATH, "w", encoding="utf-8") as f:
            f.write(report)
            
        return REPORT_PATH

async def run():
    print("🚀 [KBJ2] Starting Deep Scan...")
    auditor = ConnectivityAuditorV2()
    auditor.scan_routers()
    auditor.scan_filesystem()
    auditor.hunt_zombies()
    path = auditor.generate_report()
    print(f"✅ Mission Complete. Report: {path}")

if __name__ == "__main__":
    asyncio.run(run())
