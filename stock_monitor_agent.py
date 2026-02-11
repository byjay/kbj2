import asyncio
import argparse
import os
import sys
import json
import logging
import requests
import google.generativeai as genai
from datetime import datetime, timedelta

# --- Configuration ---
STOCK_DASHBOARD_URL = "https://isats-stock-dashboard.onrender.com"
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
LEARNING_FILE = os.path.join(DATA_DIR, "learning_data.jsonl")

# Ensure Data Dir Exists
os.makedirs(DATA_DIR, exist_ok=True)

# Load .env manually
def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value.strip()

load_env()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("⚠️  Warning: GEMINI_API_KEY not found. AI Analysis will be disabled.")

# Helper: Simple Rotating Logger
def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"📈 [StockMonitor] {timestamp} | {message}")

class StockMonitorAgent:
    def __init__(self, duration_minutes=30):
        self.duration_minutes = duration_minutes
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(minutes=duration_minutes)
        self.model = self._init_gemini()
        self.analyzed_tickers = set()

    def _init_gemini(self):
        try:
            return genai.GenerativeModel('gemini-2.0-flash')
        except:
            try:
                return genai.GenerativeModel('gemini-1.5-flash')
            except:
                return None

    def fetch_market_radar(self):
        """Fetch daily targets from Dashboard"""
        try:
            resp = requests.get(f"{STOCK_DASHBOARD_URL}/api/market/radar", timeout=10)
            if resp.status_code == 200:
                print(f"found status code 200 from {STOCK_DASHBOARD_URL}/api/market/radar")
                return resp.json()
            return []
        except Exception as e:
            log(f"Failed to fetch market radar: {e}")
            return []

    def fetch_ticker_intelligence(self, ticker):
        """Fetch existing intelligence if available"""
        try:
            resp = requests.get(f"{STOCK_DASHBOARD_URL}/api/intelligence/{ticker}", timeout=10)
            if resp.status_code == 200:
                return resp.json()
            return {}
        except:
            return {}

    async def analyze_ticker(self, ticker, data):
        """Use Gemini to analyze the situation and decide action"""
        if not self.model:
            return {"action": "HOLD", "reason": "No AI Model"}

        prompt = f"""
        Analyze this stock for immediate trading action.
        Ticker: {ticker}
        Data: {json.dumps(data)}
        Current Time: {datetime.now().isoformat()}

        Determine:
        1. Action: BUY, SELL, or HOLD
        2. Confidence: 0-100%
        3. Reason: Short concise rationale.

        Output JSON: {{ "action": "...", "confidence": ..., "reason": "..." }}
        """
        
        try:
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            text = response.text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            return json.loads(text.strip())
        except Exception as e:
            log(f"AI Analysis Failed for {ticker}: {e}")
            return {"action": "HOLD", "reason": "Error"}

    def save_learning_data(self, ticker, input_data, analysis_result):
        """Append to JSONL file"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "ticker": ticker,
            "input": input_data,
            "output": analysis_result
        }
        try:
            with open(LEARNING_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception as e:
            log(f"Failed to save learning data: {e}")

    async def run(self):
        log(f"Starting US Market Monitoring for {self.duration_minutes} minutes...")
        
        while datetime.now() < self.end_time:
            radar = self.fetch_market_radar()
            if not radar:
                log("No targets found in radar. analyzing SPY as fallback...")
                radar = [{"ticker": "SPY", "close": 0}]

            for item in radar:
                ticker = item.get("ticker", "UNKNOWN")
                if ticker in self.analyzed_tickers: continue # Basic dedupe per session

                log(f"🔍 Analyzing {ticker}...")
                intel = self.fetch_ticker_intelligence(ticker)
                
                # Merge data
                analysis_context = {**item, "intelligence": intel}
                
                # AI Decision
                decision = await self.analyze_ticker(ticker, analysis_context)
                log(f"👉 {ticker}: {decision['action']} ({decision.get('confidence')}%) - {decision.get('reason')}")
                
                # Save Data
                self.save_learning_data(ticker, analysis_context, decision)
                
                self.analyzed_tickers.add(ticker)
                await asyncio.sleep(2) # Rate limit

            # Wait before next scan
            remaining = (self.end_time - datetime.now()).total_seconds()
            if remaining <= 0: break
            
            sleep_time = min(300, remaining) # Max 5 min sleep
            log(f"Sleeping for {sleep_time:.0f}s...")
            await asyncio.sleep(sleep_time)
            self.analyzed_tickers.clear() # Reset for next cycle

        log("Monitoring Session Complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, default=30, help="Duration in minutes")
    args = parser.parse_args()
    
    agent = StockMonitorAgent(args.duration)
    asyncio.run(agent.run())
