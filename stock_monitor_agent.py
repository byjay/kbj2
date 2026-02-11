import asyncio
import argparse
import os
import sys
import json
import logging
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- Configuration ---
STOCK_DASHBOARD_URL = "https://isats-stock-dashboard.onrender.com"
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
LEARNING_FILE = os.path.join(DATA_DIR, "learning_data.jsonl")

# Ensure Data Dir Exists
os.makedirs(DATA_DIR, exist_ok=True)

# Helper: Simple Rotating Logger
def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"📈 [StockMonitor] {timestamp} | {message}")

class TechnicalAnalyzer:
    """Rule-based Heuristic Analysis Engine"""
    
    @staticmethod
    def calculate_rsi(prices, period=14):
        """Calculate Relative Strength Index"""
        if len(prices) < period + 1:
            return 50 # Neutral default
        
        deltas = np.diff(prices)
        seed = deltas[:period+1]
        up = seed[seed >= 0].sum()/period
        down = -seed[seed < 0].sum()/period
        rs = up/down if down != 0 else 0
        rsi = 100 - (100 / (1 + rs))
        
        return rsi

    def analyze(self, ticker, data):
        """
        Heuristic Decision Logic
        Based on Price Momentum, RSI (Simulated), and Market Status
        """
        price = data.get("close", 0)
        prev_price = data.get("prev_close", price)
        
        # 1. Price Momentum
        change_pct = ((price - prev_price) / prev_price) * 100 if prev_price else 0
        
        # 2. RSI Simulation (Since we get single points, we approximate/mock for now)
        # In real implementation, we would maintain a price history buffer.
        # For this agent, we use the 'intelligence' score if available, or random heuristic
        rsi = 50 
        intel = data.get("intelligence", {})
        if intel:
            # Use pre-calculated score overlap
            score = intel.get("score", 50)
            rsi = score # Treat score as RSI proxy
            
        # 3. Decision Matrix
        action = "HOLD"
        confidence = 50
        reason = "Neutral market conditions"

        if rsi > 70:
            action = "SELL"
            confidence = 75
            reason = f"Overbought conditions (RSI: {rsi:.1f}, Change: {change_pct:.2f}%)"
        elif rsi < 30:
            action = "BUY"
            confidence = 80
            reason = f"Oversold conditions (RSI: {rsi:.1f}, Change: {change_pct:.2f}%)"
        elif change_pct > 2.0:
            action = "BUY"
            confidence = 60
            reason = f"Strong upward momentum (+{change_pct:.2f}%)"
        elif change_pct < -2.0:
            action = "SELL"
            confidence = 60
            reason = f"Strong downward pressure ({change_pct:.2f}%)"
            
        return {
            "action": action,
            "confidence": confidence,
            "reason": reason,
            "indicators": {
                "rsi": rsi,
                "change_pct": round(change_pct, 2),
                "price": price
            }
        }

class StockMonitorAgent:
    def __init__(self, duration_minutes=30):
        self.duration_minutes = duration_minutes
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(minutes=duration_minutes)
        self.analyzer = TechnicalAnalyzer()
        self.analyzed_tickers = set()

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
        log(f"Starting US Market Monitoring (Heuristic Mode) for {self.duration_minutes} minutes...")
        
        while datetime.now() < self.end_time:
            radar = self.fetch_market_radar()
            if not radar:
                log("No targets found in radar. analyzing SPY as fallback...")
                radar = [{"ticker": "SPY", "close": 500.0, "prev_close": 498.0}]

            for item in radar:
                ticker = item.get("ticker", "UNKNOWN")
                if ticker in self.analyzed_tickers: continue 

                log(f"🔍 Analyzing {ticker}...")
                intel = self.fetch_ticker_intelligence(ticker)
                
                # Merge data
                analysis_context = {**item, "intelligence": intel}
                
                # Heuristic Decision
                decision = self.analyzer.analyze(ticker, analysis_context)
                log(f"👉 {ticker}: {decision['action']} ({decision.get('confidence')}%) - {decision.get('reason')}")
                
                # Save Data
                self.save_learning_data(ticker, analysis_context, decision)
                
                self.analyzed_tickers.add(ticker)
                await asyncio.sleep(1) # Rate limit

            # Wait before next scan
            remaining = (self.end_time - datetime.now()).total_seconds()
            if remaining <= 0: break
            
            sleep_time = min(60, remaining) # Max 1 min sleep
            log(f"Sleeping for {sleep_time:.0f}s...")
            await asyncio.sleep(sleep_time)
            self.analyzed_tickers.clear() 

        log("Monitoring Session Complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, default=30, help="Duration in minutes")
    args = parser.parse_args()
    
    agent = StockMonitorAgent(args.duration)
    asyncio.run(agent.run())
