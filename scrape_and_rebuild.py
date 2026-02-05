import os
import requests
from company import UniversalAgentEngine, DepartmentType

async def execute_cloning_mission():
    print("🏭 [Factory Mode] Initiating Site Reconstruction Mission...")
    print("   Target: https://www.aicitybuilders.com/")
    print("   Destination: F:\\aicitybuilders")
    
    # 1. Initialize Engine (Using 'gemini' for reliability as GLM is 401)
    engine = UniversalAgentEngine(provider="gemini")
    
    # 2. Define the Vibe (Based on extracted Meta Tags)
    site_vibe = """
    Target Style: 'AI City Builders'
    - Theme: Modern, High-Tech, Dark Mode likely (based on 'City Builders').
    - Content: AI Creator Platform, Education, Tools.
    - Structure: Landing Page, Courses (Step 1, 2, 3), FAQ.
    
    Mission: Recreate this EXACT structure but rebranded for 'SDMS Enterprise'.
    - 'AI City Builders' -> 'SDMS Enterprise'
    - 'AI Creator' -> 'Smart Drawing Management'
    - 'Step 1: AI Master' -> 'Step 1: System Master'
    - 'Step 2: Agent Beginner' -> 'Step 2: Drawing Control'
    - 'Step 3: Vibe Coding' -> 'Step 3: Factory Automation'
    """
    
    # 3. Create Directory
    target_dir = r"F:\aicitybuilders"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"   Created Directory: {target_dir}")
    
    # 4. Generate Main Landing Page (Index)
    print("\n🔨 [Builder Agent] Constructing High-Fidelity Landing Page (Index)...")
    
    index_prompt = f"""
    You are the 'Factory Builder' Agent.
    Task: Create the Main 'index.html' for SDMS Enterprise.
    
    {site_vibe}
    
    Requirements:
    - Use TailwindCSS.
    - Glassmorphism Design.
    - **CRITICAL**: Link the 3 Steps to 'step1.html', 'step2.html', 'step3.html'.
    - Hero Section: "AI Autonomous Drawing Management".
    - Footer.
    
    OUTPUT ONLY RAW HTML starting with <!DOCTYPE html>.
    """
    
    # Run Agent for Index
    idx_resp = await engine.run_agent("fac_bld_001", "Build Index", index_prompt)
    save_html(idx_resp, os.path.join(target_dir, "index.html"))
    
    # 5. Generate Sub-Pages (Step 1, 2, 3)
    pages = [
        ("step1.html", "Step 1: System Master", "Focus on Server Setup, Data Drivers, and Security."),
        ("step2.html", "Step 2: Core Agents", "Focus on the 20-Agent Org Chart, Roles (CEO, CTO, CMO), and Strategy."),
        ("step3.html", "Step 3: Factory Scale", "Focus on the 100-Agent Production Line, Scrapers, and Builders.")
    ]
    
    for filename, title, context in pages:
        print(f"\n🔨 [Builder Agent] Constructing Sub-Page '{filename}'...")
        sub_prompt = f"""
        You are the 'Factory Builder'.
        Task: Create sub-page '{filename}' for SDMS Enterprise.
        
        Theme: Consistent with Index (Dark, Glass, Tailwind).
        Title: {title}
        Context: {context}
        
        Structure:
        - Navbar (Same as Index, Link back to index.html).
        - Page Header ({title}).
        - Detailed Content Section (Use dummy text/cards for details).
        - Footer.
        
        OUTPUT ONLY RAW HTML starting with <!DOCTYPE html>.
        """
        resp = await engine.run_agent("fac_bld_001", f"Build {filename}", sub_prompt)
        save_html(resp, os.path.join(target_dir, filename))
        
def save_html(response, path):
    if response and isinstance(response, dict):
        html_code = response.get('analysis', '')
        # Simple extraction if wrapped in markdown
        if "```html" in html_code:
            html_code = html_code.split("```html")[1].split("```")[0]
        elif "```" in html_code:
            html_code = html_code.split("```")[1].split("```")[0]
            
        with open(path, "w", encoding="utf-8") as f:
            f.write(html_code.strip())
        print(f"✅ Saved: {path}")
    else:
        print(f"❌ Failed to generate {path}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(execute_cloning_mission())
