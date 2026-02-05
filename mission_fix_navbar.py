import os

# "Supreme Standard" Navigation (Designed by Commander)
NEW_NAV = """            <div class="hidden md:flex items-center space-x-6 text-sm font-medium">
                <div class="group relative">
                    <button class="text-slate-400 hover:text-white transition flex items-center gap-1 py-6">Product <i class="fas fa-chevron-down text-xs"></i></button>
                    <!-- Dropdown -->
                    <div class="absolute top-full left-0 w-64 glass rounded-xl p-2 hidden group-hover:block border border-white/10 shadow-2xl transition-all duration-300 transform translate-y-0 opacity-100 visible">
                        <div class="space-y-1">
                             <a href="step1.html" class="block px-4 py-3 rounded-lg hover:bg-white/5">
                                <div class="text-white font-bold">Analysis Engine</div>
                                <div class="text-xs text-slate-500">Auto-Audit & BOM</div>
                            </a>
                            <a href="step2.html" class="block px-4 py-3 rounded-lg hover:bg-white/5">
                                <div class="text-white font-bold">Collaboration</div>
                                <div class="text-xs text-slate-500">Team Sync & Role</div>
                            </a>
                            <a href="step3.html" class="block px-4 py-3 rounded-lg hover:bg-white/5">
                                <div class="text-white font-bold">Factory Scale</div>
                                <div class="text-xs text-slate-500">100-Agent Automation</div>
                            </a>
                        </div>
                    </div>
                </div>
                <a href="solutions.html" class="text-slate-400 hover:text-white transition">Solutions</a>
                <a href="pricing.html" class="text-slate-400 hover:text-white transition">Pricing</a>
                <a href="api_docs.html" class="text-slate-400 hover:text-white transition">API</a>
                <a href="about.html" class="text-slate-400 hover:text-white transition">Company</a>
            </div>

            <div class="flex items-center gap-4">
                <a href="contact.html" class="hidden md:block text-slate-400 hover:text-white text-sm transition font-medium">Contact</a>
                <a href="contact.html" class="bg-blue-600 text-white px-5 py-2 rounded-full text-sm font-bold hover:bg-blue-500 transition shadow-lg shadow-blue-900/40">Get Started</a>
            </div>"""

def run_agent_fix():
    print("🤖 [Builder_07] Received Order: 'Refactor Index Navigation'")
    
    target_file = r"F:\aicitybuilders\index.html"
    
    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Locate the target block (using a wider, safer search or explicit markers if possible)
    # Strategy: Find the start of the menu container and the end of the button container
    start_marker = '<div class="hidden md:flex items-center space-x-10 text-sm font-medium">'
    end_marker = 'class="bg-slate-800 text-white px-5 py-2 rounded-full text-sm font-bold hover:bg-slate-700 transition">Dashboard</a>'
    
    if start_marker in content:
        # We found the specific point to replace
        # We need to find the closing div of the button container to restart safe splice?
        # Actually, let's just find the start marker and the end of the `nav` container essentially.
        
        # Simpler approach: Locate the specific old block and replace it.
        # Based on file read:
        old_block_start = content.find(start_marker)
        
        # Find the closing </div> of the SECOND container (the buttons)
        # It's risky to rely on counting divs.
        # Let's try to replace the whole inner part of the nav if we can target it.
        
        # New Strategy: Read strictly between "Link Start" and "Link End" known strings.
        # Start: 'class="font-bold text-2xl tracking-tighter text-slate-100 group-hover:text-white transition">SDMS</span>'
        # End: '</div>\n    </nav>'
        
        anchor_start = 'class="font-bold text-2xl tracking-tighter text-slate-100 group-hover:text-white transition">SDMS</span>'
        anchor_end = '</nav>'
        
        s_idx = content.find(anchor_start)
        e_idx = content.find(anchor_end, s_idx)
        
        if s_idx != -1 and e_idx != -1:
            # We skip the </a> closing tag
            real_start = content.find('</a>', s_idx) + 4
            
            # Construct the new middle part
            new_content = content[:real_start] + "\n\n" + NEW_NAV + "\n        </div>\n" + content[e_idx:]
            
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            print("✅ [Builder_07] Navigation Patch Applied Successfully.")
        else:
             print("❌ [Builder_07] Error: Anchors not found. Requesting Manual Override.")
    else:
        print(f"❌ [Builder_07] Error: Could not find start marker: {start_marker}")

if __name__ == "__main__":
    run_agent_fix()
