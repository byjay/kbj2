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
            
        # 3. Decision Matrix (Conservative Mode for 3% Target)
        action = "HOLD"
        confidence = 50
        reason = "Monitoring market pulse..."

        # Conservative BUY: Extreme oversold OR massive breakout with volume
        if rsi < 25:
            action = "BUY"
            confidence = 85
            reason = f"🔥 High Conviction Oversold (RSI: {rsi:.1f})"
        elif change_pct > 3.5:
            action = "BUY"
            confidence = 80
            reason = f"🚀 Momentum Breakout (+{change_pct:.2f}%)"

        # Strategic SELL: Extreme overbought OR hitting targets
        elif rsi > 75:
            action = "SELL"
            confidence = 85
            reason = f"⚠️ Overbought Alert (RSI: {rsi:.1f})"
        elif change_pct < -3.0:
            action = "SELL"
            confidence = 70
            reason = f"📉 Protecting Capital: Trend reversal ({change_pct:.2f}%)"
            
        # Target Exit: Check if current gain is near or above terminal target (3%)
        # In real account, we'd check average purchase price, but here we use session change
        if action == "HOLD" and change_pct >= 3.0:
            action = "SELL"
            confidence = 90
            reason = f"🎯 Profit Target Reached: +{change_pct:.2f}% (Daily Goal: 3%)"
            
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

class ExecutionEngine:
    """Handles order execution via Dashboard API"""
    
    def __init__(self, api_url):
        self.api_url = api_url

    def execute_trade(self, ticker, action, confidence, price):
        """Send order to Dashboard API"""
        if confidence < 80:
            return False
            
        log(f"🚀 [Execution] Sending {action} order for {ticker} (Confidence: {confidence}%)")
        
        # Strict US Market Enforcement
        is_us = any(c.isalpha() for c in ticker) or len(ticker) > 6
        if not is_us:
            log(f"⚠️ [Execution] Blocking KR Trade request for {ticker}. US Market Only.")
            return False
            
        market = "US"
            
        payload = {
            "ticker": ticker,
            "action": action,
            "quantity": 10 if market == "KR" else 1, # Small test quantity
            "price": 0, # Market order
            "market": market
        }
        
        try:
            resp = requests.post(f"{self.api_url}/api/order", json=payload, timeout=15)
            if resp.status_code == 200:
                result = resp.json()
                log(f"✅ Trade Successful: {result.get('order_no')}")
                return True
            else:
                log(f"❌ Trade Failed: {resp.text}")
                return False
        except Exception as e:
            log(f"🔥 Execution Error: {e}")
            return False

class StockMonitorAgent:
    def __init__(self, duration_minutes=30):
        self.duration_minutes = duration_minutes
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(minutes=duration_minutes)
        self.analyzer = TechnicalAnalyzer()
        self.executor = ExecutionEngine(STOCK_DASHBOARD_URL)
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
        log(f"Starting 24/7 US Market Monitoring (Heuristic Mode)...")
        
        while True: # Eternal Loop for Server Session
            # Control: Only run during active window or if forced
            # (Night Shift logic in continuous_dev handles the 13:00-21:00 UTC window)
            
            radar = self.fetch_market_radar()
            has_explosion = any(item.get("source") == "EXPLOSION_SCANNER" for item in radar)
            
            if not radar:
                log("No targets found in radar. analyzing SPY as fallback...")
                radar = [{"ticker": "SPY", "close": 500.0, "prev_close": 498.0, "source": "FALLBACK"}]

            for item in radar:
                ticker = item.get("ticker", "UNKNOWN")
                source = item.get("source", "UNKNOWN")
                
                # --- Strict US Market Filter ---
                is_us_stock = any(c.isalpha() for c in ticker) or len(ticker) > 6
                if not is_us_stock:
                    continue 
                
                if ticker in self.analyzed_tickers: continue 

                log(f"🔍 Analyzing US Stock [{source}]: {ticker}...")
                intel = self.fetch_ticker_intelligence(ticker)
                
                # Merge data
                analysis_context = {**item, "intelligence": intel}
                
                # Heuristic Decision
                decision = self.analyzer.analyze(ticker, analysis_context)
                
                # Bonus confidence for Explosion targets
                if source == "EXPLOSION_SCANNER":
                    decision["confidence"] = min(100, decision["confidence"] + 5)
                    log(f"⚡ [Explosion Bonus] Boosted confidence for {ticker}")

                log(f"👉 {ticker}: {decision['action']} ({decision.get('confidence')}%) - {decision.get('reason')}")
                
                # Execute Trade if High Confidence
                if decision["action"] in ["BUY", "SELL"]:
                    self.executor.execute_trade(
                        ticker, 
                        decision["action"], 
                        decision["confidence"], 
                        decision["indicators"]["price"]
                    )
                
                # Save Data
                self.save_learning_data(ticker, analysis_context, decision)
                
                self.analyzed_tickers.add(ticker)
                await asyncio.sleep(1) # Rate limit

            # Recycle tickers for fresh analysis
            self.analyzed_tickers.clear() 
            
            # Wait before next scan
            remaining = (self.end_time - datetime.now()).total_seconds()
            if remaining <= 0: break
            
            # Faster polling if market is exploding
            interval = 30 if has_explosion else 60
            sleep_time = min(interval, remaining) 
            log(f"Sleeping for {sleep_time:.0f}s... (Explosion Mode: {has_explosion})")
            await asyncio.sleep(sleep_time)

        log("Monitoring Session Complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, default=30, help="Duration in minutes")
    args = parser.parse_args()
    
    agent = StockMonitorAgent(args.duration)
    asyncio.run(agent.run())
