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

# --- ISATS Core Paths ---
# Ensure we can import savage logic from the Ferrari codebase
sys.path.append(r"F:\genmini\stock")
sys.path.append(r"F:\genmini\stock\ISATS_Ferrari\core")

try:
    from signal_validator_savage import SignalValidator
    HAS_VALIDATOR = True
except ImportError:
    HAS_VALIDATOR = False
    log("⚠️ SignalValidator not found in F:/genmini/stock. Performance may degrade.")


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
    """Handles order execution via Dashboard API with Scaled Strategy support"""
    
    def __init__(self, api_url):
        self.api_url = api_url
        self.validator = SignalValidator() if HAS_VALIDATOR else None
        self.active_scaled_exits = {} # ticker -> task

    def execute_trade(self, ticker, action, confidence, price, analysis_context=None):
        """Send order to Dashboard API with Scaled Entry logic for BUY"""
        if confidence < 80:
            return False
            
        # 🛡️ Pre-flight Validation (Savage Edition)
        if action == "BUY" and self.validator:
            # We need to simulate the market_data and timeframe_data structure expected by Validator
            # For now, we use a simplified mock based on the intelligence score
            mock_market_data = {'Close': price, 'Volume': analysis_context.get('volume', 100000)}
            # Mocking timeframe data for now - in production this would be real history
            mock_timeframe_data = pd.DataFrame([mock_market_data] * 30) 
            
            is_valid, reason = self.validator.validate(ticker, mock_market_data, mock_timeframe_data)
            if not is_valid:
                log(f"🚫 [Validator] Blocked {ticker}: {reason}")
                return False
            log(f"🛡️ [Validator] Passed {ticker}: {reason}")

        log(f"🚀 [Execution] Initiating {action} for {ticker} (Confidence: {confidence}%)")
        
        # Strict US Market Enforcement
        is_us = any(c.isalpha() for c in ticker) or len(ticker) > 6
        if not is_us:
            log(f"⚠️ [Execution] Blocking KR Trade request for {ticker}. US Market Only.")
            return False
            
        market = "US"
        
        if action == "BUY":
            # Initiate Scaled Entry (Async)
            asyncio.create_task(self._scaled_entry(ticker, confidence, market))
            return True
        else:
            # Simple SELL for non-scaled or emergency
            return self._place_order(ticker, "SELL", 1, 0, market)

    async def _scaled_entry(self, ticker, confidence, market):
        """Scaled Entry Logic (Reimplemented from Savage Engine)"""
        splits = 3 if confidence > 0.85 else 2 # Conservative for 3% target
        log(f"⚖️ [SCALING] Initiating {splits}-part entry for {ticker}")
        
        for i in range(splits):
            success = self._place_order(ticker, "BUY", 1, 0, market)
            if success:
                log(f"✅ [Scaled-Entry] Step {i+1}/{splits} FILLED for {ticker}")
            await asyncio.sleep(5) # Inter-step delay
            
        # After full entry, start Scaled Exit monitoring
        asyncio.create_task(self._monitor_scaled_exit(ticker, market))

    async def _monitor_scaled_exit(self, ticker, market):
        """1-5-9 Split Exit Strategy (Simplified for selective 3% goal)"""
        log(f"🎯 [Monitor] Starting Scaled Exit monitoring for {ticker}")
        
        # To calculate profit, we need the initial average price
        # In this mock/heuristic mode, we'll fetch current balance or assume entry price
        # We'll use polling to simulate the Savage Engine's behavior
        
        entry_price = 0
        while entry_price == 0:
            # Fetch current quote as entry price approximation
            resp = requests.get(f"{STOCK_DASHBOARD_URL}/api/intelligence/{ticker}")
            if resp.status_code == 200:
                entry_price = resp.json().get("close", 0)
            await asyncio.sleep(2)

        start_time = datetime.now()
        sold_l1 = False
        
        while True:
            # Check price
            resp = requests.get(f"{STOCK_DASHBOARD_URL}/api/intelligence/{ticker}")
            if resp.status_code != 200:
                await asyncio.sleep(5)
                continue
                
            curr_price = resp.json().get("close", 0)
            if curr_price == 0: continue
            
            profit_pct = (curr_price - entry_price) / entry_price * 100 if entry_price else 0
            
            # 1-5-9 Strategy Adjusted for 3% Selective Target
            # Level 1: +1.5% (Secure partial)
            if not sold_l1 and profit_pct >= 1.5:
                log(f"💰 [EXIT-L1] {ticker} @ +{profit_pct:.2f}% (Target 1.5%).")
                # In real setup, we'd sell % qty. Here we just send another order.
                self._place_order(ticker, "SELL", 1, 0, market)
                sold_l1 = True
            
            # Goal Reached: +3% (Liquidate)
            if profit_pct >= 3.0:
                log(f"🎯 [Goal Reached] {ticker} @ +{profit_pct:.2f}%. Liquidating.")
                self._place_order(ticker, "SELL", 1, 0, market)
                break
                
            # Hard Stop Loss: -1.5%
            if profit_pct <= -1.5:
                log(f"🚨 [Stop-Loss] {ticker} @ {profit_pct:.2f}%. Protecting capital.")
                self._place_order(ticker, "SELL", 1, 0, market)
                break
                
            # Time limit: 2 hours
            if (datetime.now() - start_time).total_seconds() > 7200:
                log(f"🕒 [Time-Exit] 2h limit reached for {ticker}.")
                self._place_order(ticker, "SELL", 1, 0, market)
                break
                
            await asyncio.sleep(10)

    def _place_order(self, ticker, action, quantity, price, market):
        """Helper to send the actual order payload"""
        payload = {
            "ticker": ticker,
            "action": action,
            "quantity": quantity,
            "price": price,
            "market": market
        }
        try:
            resp = requests.post(f"{self.api_url}/api/order", json=payload, timeout=15)
            return resp.status_code == 200
        except Exception as e:
            log(f"Order Placement Error: {e}")
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
                        decision["indicators"]["price"],
                        analysis_context=analysis_context
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
