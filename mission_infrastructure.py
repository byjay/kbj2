import os
import sys
import time
import asyncio

# FORCE UTF-8 OUTPUT (Windows Check)
sys.stdout.reconfigure(encoding='utf-8')

# Mission: Establish Corporate Email Infrastructure Documentation
# Commander: User / Antigravity
# Executor: Agent_Infra_01

GUIDE_CONTENT = """# SEDMS Enterprise: Corporate Email Infrastructure Guide 📧

**Objective**: Establish Professional Email (`contact@sedms.app`, `ceo@sedms.app`) for **$0/month**.
**Solution**: **Cloudflare Email Routing** (Forwarding) + **Gmail SMTP** (Send As).

---

## 🏗️ Architecture
- **Inbound**: `contact@sedms.app` -> Cloudflare -> Forwards to `your_personal@gmail.com`
- **Outbound**: `Gmail` -> "Send As `contact@sedms.app`" (via App Password).

## 🚀 Step-by-Step Implementation

### Phase 1: Inbound Setup (Cloudflare)
1.  **Log in** to your Cloudflare Dashboard (Manage `sedms.app`).
2.  Go to **Email** > **Email Routing** on the left sidebar.
3.  Click **"Enable Email Routing"**.
    - Cloudflare will ask to add DNS Records (MX, SPF). Value: `Auto-Configure`.
4.  **Create Custom Addresses**:
    - Click **"Routes"** > **"Create Address"**.
    - **Custom Address**: `contact` @ `sedms.app`
    - **Destination**: `[Your Actual Gmail Address]`
    - Repeat for `ceo` @ `sedms.app`.
5.  **Verify**: Check your Gmail. You will get a "Verify Email Routing" link. Click it.
    - *Result*: Emails sent to `contact@sedms.app` will now land in your Gmail.

### Phase 2: Outbound Setup (Gmail "Send As")
1.  **Google Account Security**:
    - Go to [Google Account Security](https://myaccount.google.com/security).
    - Enable **2-Step Verification** (if not on).
    - Search for **"App Passwords"**.
    - Create New App Password:
        - App: `Mail`
        - Device: `Mac` (or Custom name "SEDMS").
        - **Copy the 16-digit code**. (e.g., `xxxx xxxx xxxx xxxx`)
2.  **Gmail Settings**:
    - Open Gmail > Settings (⚙️) > **See all settings**.
    - Go to **Accounts and Import** tab.
    - Under "Send mail as", click **"Add another email address"**.
3.  **Configure Alias**:
    - **Name**: `SEDMS Support` (or `CEO of SEDMS`).
    - **Email**: `contact@sedms.app`.
    - **Treat as an alias**: [x] CHECKED.
    - Click **Next Step**.
4.  **SMTP Settings** (Crucial Step):
    - **SMTP Server**: `smtp.gmail.com`
    - **Port**: `587`
    - **Username**: `[Your Actual Gmail Address]` (Not the sedms one).
    - **Password**: (**Paste the 16-digit App Password**).
    - **TLS**: Secured connection using TLS.
    - Click **Add Account**.
5.  **Final Verification**:
    - Gmail sends a code to `contact@sedms.app`.
    - Since Phase 1 is done, check your inbox, get the code, and confirm.

### Phase 3: Brand Polish
- Go to Gmail Settings > General.
- Create a **Signature** for your new alias:
  ```
  Best regards,
  
  **Your Name**
  Head of Engineering | SEDMS Enterprise
  🌐 [www.sedms.app](https://sedms.app)
  ```
"""

def execute_mission():
    print("📡 [COMMANDER] Mission: 'Establish Email Protocol'.")
    print(f"Assigning to: **Agent_Infra_01** (Cloudflare Specialist)...")
    time.sleep(1)
    
    target_dir = os.getenv("KBJ2_TARGET_DIR", r"F:\kbj2")
    # If target is not kbj2, put guide inside target too
    target_file = os.path.join(target_dir, "SEDMS_EMAIL_SETUP_GUIDE.md")
    
    print(f"🏗️  [Agent_Infra_01] Researching Cloudflare Routing...")
    time.sleep(0.5)
    print(f"📝 [Agent_Infra_01] Drafting Documentation...")
    
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(GUIDE_CONTENT)
        
    print(f"✅ [Agent_Infra_01] Mission Complete. Guide saved to: {target_file}")
    print(f"   Status: READY FOR DEPLOYMENT.")

if __name__ == "__main__":
    execute_mission()
