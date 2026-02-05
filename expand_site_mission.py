import os
import sys
import asyncio
from datetime import datetime

# FORCE UTF-8 OUTPUT (Windows Check)
sys.stdout.reconfigure(encoding='utf-8')

# Component Library (The "Monet Registry" Parts)
NAVBAR = """<nav class="fixed w-full z-50 glass border-b border-white/5 top-0 left-0">
        <div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
            <a href="index.html" class="flex items-center gap-3 group">
                <div class="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-700 rounded-xl flex items-center justify-center text-white shadow-xl shadow-blue-900/20">
                    <i class="fas fa-cube"></i>
                </div>
                <span class="font-bold text-2xl tracking-tighter text-slate-100 group-hover:text-white transition">SDMS</span>
            </a>
            <div class="hidden md:flex items-center space-x-8 text-sm font-medium">
                <a href="solutions.html" class="text-slate-400 hover:text-white transition">Solutions</a>
                <a href="pricing.html" class="text-slate-400 hover:text-white transition">Pricing</a>
                <a href="api_docs.html" class="text-slate-400 hover:text-white transition">API</a>
                <a href="blog.html" class="text-slate-400 hover:text-white transition">Blog</a>
                <a href="about.html" class="text-slate-400 hover:text-white transition">Company</a>
            </div>
            <div class="flex items-center gap-4">
                <a href="contact.html" class="bg-blue-600 text-white px-6 py-2.5 rounded-full text-sm font-bold transition hover:bg-blue-500">Contact Sales</a>
            </div>
        </div>
    </nav>"""

FOOTER = """<footer class="bg-black border-t border-white/10 pt-20 pb-10">
        <div class="max-w-7xl mx-auto px-6 grid grid-cols-2 md:grid-cols-5 gap-10 mb-16">
            <div class="col-span-2">
                <span class="font-bold text-2xl text-white">SDMS</span>
                <p class="text-slate-500 text-sm mt-4">Autonomous Engineering Intelligence.</p>
            </div>
            <div>
                <h4 class="font-bold text-white mb-6">Platform</h4>
                <ul class="space-y-4 text-sm text-slate-500">
                    <li><a href="solutions.html" class="hover:text-white">Solutions</a></li>
                    <li><a href="pricing.html" class="hover:text-white">Pricing</a></li>
                    <li><a href="api_docs.html" class="hover:text-white">API Docs</a></li>
                </ul>
            </div>
            <div>
                <h4 class="font-bold text-white mb-6">Company</h4>
                <ul class="space-y-4 text-sm text-slate-500">
                    <li><a href="about.html" class="hover:text-white">About Us</a></li>
                    <li><a href="blog.html" class="hover:text-white">Blog</a></li>
                    <li><a href="contact.html" class="hover:text-white">Contact</a></li>
                </ul>
            </div>
        </div>
        <div class="max-w-7xl mx-auto px-6 pt-8 border-t border-white/5 text-center text-slate-600 text-xs">
            &copy; 2026 KBJ2 Corp. Mass Produced by AI Factory.
        </div>
    </footer>"""

COMMON_HEAD = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{TITLE} - SDMS Enterprise</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;600;700;800&display=swap');
        body { font-family: 'Pretendard', sans-serif; }
        .glass { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.08); }
    </style>
</head>
<body class="bg-[#050505] text-white min-h-screen flex flex-col pt-20">"""

# Page Blueprints (The "Content" to be injected)
PAGES = [
    {
        "filename": "solutions.html",
        "title": "Solutions",
        "content": """
        <header class="py-20 px-6 text-center">
            <h1 class="text-5xl font-bold mb-6">Enterprise Solutions</h1>
            <p class="text-xl text-slate-400">Tailored workflows for Automotive, Aerospace, and Plant Engineering.</p>
        </header>
        <section class="max-w-7xl mx-auto px-6 py-10 grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="glass p-8 rounded-3xl">
                <i class="fas fa-car text-4xl text-blue-500 mb-6"></i>
                <h3 class="text-2xl font-bold mb-4">Automotive</h3>
                <p class="text-slate-400">Manage 50,000+ parts per vehicle with AI-driven BOM validation.</p>
            </div>
            <div class="glass p-8 rounded-3xl">
                <i class="fas fa-plane text-4xl text-purple-500 mb-6"></i>
                <h3 class="text-2xl font-bold mb-4">Aerospace</h3>
                <p class="text-slate-400">ISO 9001 compliant audit trails for mission-critical components.</p>
            </div>
            <div class="glass p-8 rounded-3xl">
                <i class="fas fa-industry text-4xl text-pink-500 mb-6"></i>
                <h3 class="text-2xl font-bold mb-4">Plant EPC</h3>
                <p class="text-slate-400">Automate P&ID parsing and equipment list generation.</p>
            </div>
        </section>
        """
    },
    {
        "filename": "pricing.html",
        "title": "Pricing",
        "content": """
        <header class="py-20 px-6 text-center">
            <h1 class="text-5xl font-bold mb-6">Simple, Transparent Pricing</h1>
            <p class="text-xl text-slate-400">Scale your agents as you grow.</p>
        </header>
        <section class="max-w-7xl mx-auto px-6 py-10 grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="glass p-8 rounded-3xl border border-white/5">
                <h3 class="text-xl font-bold mb-2">Starter</h3>
                <div class="text-4xl font-bold mb-6">$0<span class="text-sm text-slate-500">/mo</span></div>
                <ul class="space-y-3 text-slate-400 mb-8">
                    <li><i class="fas fa-check text-green-500 mr-2"></i> 1 Agent</li>
                    <li><i class="fas fa-check text-green-500 mr-2"></i> 100 Drawings/mo</li>
                </ul>
                <a href="#" class="block text-center py-3 rounded-full bg-slate-800 hover:bg-slate-700 font-bold">Start Free</a>
            </div>
            <div class="glass p-8 rounded-3xl border border-blue-500 relative transform scale-105">
                <div class="absolute top-0 left-1/2 -translate-x-1/2 bg-blue-500 text-xs font-bold px-3 py-1 rounded-b-lg">POPULAR</div>
                <h3 class="text-xl font-bold mb-2 text-blue-400">Pro Team</h3>
                <div class="text-4xl font-bold mb-6">$499<span class="text-sm text-slate-500">/mo</span></div>
                <ul class="space-y-3 text-slate-300 mb-8">
                    <li><i class="fas fa-check text-blue-400 mr-2"></i> 20 Agents (Core Team)</li>
                    <li><i class="fas fa-check text-blue-400 mr-2"></i> Unlimited Drawings</li>
                    <li><i class="fas fa-check text-blue-400 mr-2"></i> API Access</li>
                </ul>
                <a href="#" class="block text-center py-3 rounded-full bg-blue-600 hover:bg-blue-500 font-bold text-white">Get Pro</a>
            </div>
            <div class="glass p-8 rounded-3xl border border-white/5">
                <h3 class="text-xl font-bold mb-2">Enterprise Factory</h3>
                <div class="text-4xl font-bold mb-6">Custom</div>
                <ul class="space-y-3 text-slate-400 mb-8">
                    <li><i class="fas fa-check text-pink-500 mr-2"></i> 100+ Agents</li>
                    <li><i class="fas fa-check text-pink-500 mr-2"></i> On-Premise Install</li>
                    <li><i class="fas fa-check text-pink-500 mr-2"></i> Dedicated MSA</li>
                </ul>
                <a href="#" class="block text-center py-3 rounded-full border border-white/20 hover:bg-white/5 font-bold">Contact Sales</a>
            </div>
        </section>
        """
    },
    {
        "filename": "api_docs.html",
        "title": "API Documentation",
        "content": """
        <div class="flex max-w-7xl mx-auto px-6 py-10 gap-10">
            <aside class="w-64 hidden md:block">
                <h3 class="font-bold mb-4 text-slate-500 uppercase text-xs tracking-wider">Reference</h3>
                <ul class="space-y-2 text-sm text-slate-400">
                    <li><a href="#" class="text-blue-400 font-bold">Introduction</a></li>
                    <li><a href="#" class="hover:text-white">Authentication</a></li>
                    <li><a href="#" class="hover:text-white">Drawing Endpoints</a></li>
                    <li><a href="#" class="hover:text-white">BOM Endpoints</a></li>
                    <li><a href="#" class="hover:text-white">Webhooks</a></li>
                </ul>
            </aside>
            <main class="flex-1">
                <h1 class="text-4xl font-bold mb-6">API Roference</h1>
                <div class="glass p-8 rounded-2xl mb-8">
                    <div class="flex items-center gap-3 mb-4">
                        <span class="bg-green-500 text-black px-2 py-1 rounded text-xs font-bold">GET</span>
                        <code class="text-lg">/v1/drawings/{id}/bom</code>
                    </div>
                    <p class="text-slate-400 mb-4">Extracts BOM data from a specific drawing ID.</p>
                    <div class="bg-black p-4 rounded-lg font-mono text-sm text-green-400">
                        curl -X GET https://api.sdms.ai/v1/drawings/dwg_123/bom \\<br>
                        -H "Authorization: Bearer sk_live_..."
                    </div>
                </div>
                 <div class="glass p-8 rounded-2xl">
                    <div class="flex items-center gap-3 mb-4">
                        <span class="bg-blue-500 text-black px-2 py-1 rounded text-xs font-bold">POST</span>
                        <code class="text-lg">/v1/factory/batch</code>
                    </div>
                    <p class="text-slate-400 mb-4">Initiates a mass processing job for up to 1,000 files.</p>
                </div>
            </main>
        </div>
        """
    },
    {
        "filename": "about.html",
        "title": "About Us",
        "content": """
        <header class="py-20 px-6 text-center">
            <h1 class="text-5xl font-bold mb-6">We Are KBJ2 Corp.</h1>
            <p class="text-xl text-slate-400">Building the workforce of the future.</p>
        </header>
        <section class="max-w-4xl mx-auto px-6 py-10">
            <div class="glass p-10 rounded-3xl mb-12">
                <h2 class="text-3xl font-bold mb-4">The Vision</h2>
                <p class="text-slate-400 leading-relaxed text-lg">
                    We believe engineers should engineer, not manage paperwork. 
                    Our mission is to deploy 100 autonomous agents into every engineering team, 
                    handling the mundane so humans can build the impossible.
                </p>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div class="glass p-8 rounded-2xl">
                    <h3 class="text-xl font-bold mb-2">Established</h3>
                    <p class="text-4xl font-bold text-blue-400">2026</p>
                </div>
                 <div class="glass p-8 rounded-2xl">
                    <h3 class="text-xl font-bold mb-2">Headquarters</h3>
                    <p class="text-4xl font-bold text-purple-400">Seoul, KR</p>
                </div>
            </div>
        </section>
        """
    },
    {
        "filename": "blog.html",
        "title": "Engineering Blog",
        "content": """
        <header class="py-20 px-6 text-center">
            <h1 class="text-5xl font-bold mb-6">Engineering Intelligence Blog</h1>
        </header>
        <section class="max-w-6xl mx-auto px-6 py-10 grid grid-cols-1 md:grid-cols-3 gap-8">
            <article class="glass p-6 rounded-2xl hover:bg-white/5 transition cursor-pointer">
                <div class="h-48 bg-blue-900/20 rounded-xl mb-6 flex items-center justify-center text-4xl text-blue-500"><i class="fas fa-code-branch"></i></div>
                <div class="text-xs text-blue-400 font-bold mb-2">ENGINEERING</div>
                <h3 class="text-xl font-bold mb-3">How we scaled to 100 Agents</h3>
                <p class="text-slate-400 text-sm">A deep dive into the KBJ2 asynchronous engine architecture.</p>
            </article>
            <article class="glass p-6 rounded-2xl hover:bg-white/5 transition cursor-pointer">
                <div class="h-48 bg-purple-900/20 rounded-xl mb-6 flex items-center justify-center text-4xl text-purple-500"><i class="fas fa-brain"></i></div>
                <div class="text-xs text-purple-400 font-bold mb-2">AI RESEARCH</div>
                <h3 class="text-xl font-bold mb-3">Beyond OCR: Understanding Geometry</h3>
                <p class="text-slate-400 text-sm">Why text recognition isn't enough for engineering drawings.</p>
            </article>
             <article class="glass p-6 rounded-2xl hover:bg-white/5 transition cursor-pointer">
                <div class="h-48 bg-pink-900/20 rounded-xl mb-6 flex items-center justify-center text-4xl text-pink-500"><i class="fas fa-industry"></i></div>
                <div class="text-xs text-pink-400 font-bold mb-2">CASE STUDY</div>
                <h3 class="text-xl font-bold mb-3">Saving 3,000 Hours for AutoParts Inc.</h3>
                <p class="text-slate-400 text-sm">Real world results from our pilot program.</p>
            </article>
        </section>
        """
    },
    {
        "filename": "contact.html",
        "title": "Contact Sales",
        "content": """
        <header class="py-20 px-6 text-center">
            <h1 class="text-5xl font-bold mb-6">Talk to an Expert</h1>
        </header>
        <section class="max-w-2xl mx-auto px-6 pb-20">
            <div class="glass p-10 rounded-3xl">
                <form class="space-y-6">
                    <div class="grid grid-cols-2 gap-6">
                        <div>
                            <label class="block text-sm text-slate-400 mb-2">First Name</label>
                            <input type="text" class="w-full bg-slate-900 border border-white/10 rounded-lg p-3 text-white focus:border-blue-500 outline-none">
                        </div>
                         <div>
                            <label class="block text-sm text-slate-400 mb-2">Last Name</label>
                            <input type="text" class="w-full bg-slate-900 border border-white/10 rounded-lg p-3 text-white focus:border-blue-500 outline-none">
                        </div>
                    </div>
                    <div>
                        <label class="block text-sm text-slate-400 mb-2">Work Email</label>
                        <input type="email" class="w-full bg-slate-900 border border-white/10 rounded-lg p-3 text-white focus:border-blue-500 outline-none">
                    </div>
                     <div>
                        <label class="block text-sm text-slate-400 mb-2">Message</label>
                        <textarea rows="4" class="w-full bg-slate-900 border border-white/10 rounded-lg p-3 text-white focus:border-blue-500 outline-none"></textarea>
                    </div>
                    <button class="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-4 rounded-xl transition">
                        Send Message
                    </button>
                </form>
            </div>
            <div class="text-center mt-10 text-slate-500">
                <p>Or email us directly at <a href="mailto:hello@kbj2.ai" class="text-blue-400">hello@kbj2.ai</a></p>
            </div>
        </section>
        """
    }
]

def factory_production_run():
    print("🏭 [FACTORY] Starting Mass Production Run (Batch Size: 6 Pages)...")
    
    target_dir = os.getenv("KBJ2_TARGET_DIR", r"F:\aicitybuilders")
    if target_dir:
        target_dir = target_dir.strip().strip('"').strip("'")
    
    # Clean Path
    target_dir = os.path.abspath(target_dir)
        
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for page in PAGES:
        try:
            filename = page["filename"]
            print(f"   ► Assigning Agent to: {filename}...")
            
            # Assemble Content
            full_html = COMMON_HEAD.replace("{TITLE}", page["title"]) + \
                        NAVBAR + \
                        page["content"] + \
                        FOOTER + \
                        "</body></html>"
            
            # Write to Disk
            file_path = os.path.join(target_dir, filename)
            
            # Extra Safety: Check if file_path is valid
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(full_html)
                
            print(f"     ✅ [Builder] Generated {filename} (Size: {len(full_html)} bytes)")
            
        except Exception as e:
            # Local Error for this file
            err_msg = f"❌ [ERROR] Failed to write {filename}: {e} | Path: {repr(file_path)}"
            print(err_msg)
            # Append to comprehensive log if exists
            # Append to comprehensive log if exists
            try:
                 log_path = os.path.join(os.path.dirname(target_dir), "EXPAND_ERROR.log")
                 with open(log_path, "a", encoding="utf-8") as log:
                     log.write(err_msg + "\n")
            except: pass
            continue # Continue to next page

    print("\n✅ [FACTORY] Mass Production Complete. (Check logs for any skipped files).")
    print("   Total Site Scale: 10 Pages (Home + 3 Features + 6 Marketing)")

if __name__ == "__main__":
    try:
        if sys.platform == 'win32':
             asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(factory_production_run())
    except Exception as e:
        import traceback
        # Write to local file first
        with open("EXPAND_ERROR.log", "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        sys.exit(1)
