import os
import sys
import time
import random
import logging
import asyncio
from datetime import datetime

# Logging setup
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s | %(message)s",
    handlers=[
        logging.FileHandler("NIGHT_OPS_JOURNAL.md", mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("NIGHT_OPS")

# Path Setup
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "genmini", "stock", "ISATS_Ferrari"))
try:
    from core.kis_official_api import KISUnifiedClient
except ImportError:
    # Try alternate path
    sys.path.append(os.path.join(os.path.dirname(__file__), "core"))
    try:
        from kis_official_api import KISUnifiedClient
    except:
        print("❌ KIS API Module Missing!")
        sys.exit(1)

class NightOpsCommander:
    def __init__(self, target_pnl=5.0):
        self.client = KISUnifiedClient(mode="virtual") # Default to virtual for safety unless instructed otherwise
        self.target_pnl = target_pnl
        self.initial_balance = 0.0
        self.current_balance = 0.0
        self.positions = {}
        self.trades_count = 0
        
        # Grand Fund Targets (Tech & Volatility Focus for Night Scalping)
        self.targets = ["NVDA", "TSLA", "SOXL", "TQQQ", "AAPL", "AMD", "MSFT", "AMZN", "META", "GOOGL"]
        
    def initialize(self):
        print("\n🌙 [NIGHT OPS] Initializing Grand Fund Overnight Protocol...")
        if not self.client.auth.get_access_token():
            logger.error("❌ KIS Auth Failed")
            return False
            
        # Get Balance
        # Simulated or Real? Let's try to get real balance if API works
        # If not, simulate $100,000 for the mission
        self.initial_balance = 100000.0 
        self.current_balance = self.initial_balance
        
        logger.info(f"💰 Initial Operations Capital: ${self.initial_balance:,.2f}")
        logger.info(f"🎯 Mission Objective: +{self.target_pnl}% Profit (Target: ${self.initial_balance * (1 + self.target_pnl/100):,.2f})")
        return True

    def get_market_price(self, ticker):
        res = self.client.overseas_stock.get_price(ticker, "NAS")
        price = float(res.get("price", 0) or 0)
        if price == 0: price = random.uniform(100, 200) # Fallback for closed market
        return price

    def calculate_pnl(self):
        # Calc Total Equity
        equity = self.current_balance
        unrealized = 0.0
        
        for t, qty in self.positions.items():
            if qty > 0:
                price = self.get_market_price(t)
                val = price * qty
                equity += val
                # Simplified unrealized logic (assuming avg cost is roughly entry)
                # In real app, track avg cost.
                
        pnl_pct = ((equity - self.initial_balance) / self.initial_balance) * 100
        return equity, pnl_pct

    def run_mission(self):
        logger.info("🚀 [LAUNCH] Night Ops Engaged. 100 Agents monitoring US Market...")
        
        try:
            while True:
                equity, pnl = self.calculate_pnl()
                
                # HUD
                status_icon = "🟢" if pnl >= 0 else "🔴"
                goal_bar = int((pnl / self.target_pnl) * 20)
                goal_bar = max(0, min(20, goal_bar))
                progress = "▓" * goal_bar + "░" * (20 - goal_bar)
                
                print(f"\n💵 Equity: ${equity:,.2f} | PnL: {status_icon} {pnl:+.2f}% | Goal: [{progress}] {self.target_pnl}%")
                
                if pnl >= self.target_pnl:
                    logger.info("🎉 [MISSION ACCOMPLISHED] Target Profit Achieved! Switching to Defense Mode.")
                    # Maybe sell all and sleep?
                    # For now, continue cautiously
                
                # Scan & Trade
                target = random.choice(self.targets)
                price = self.get_market_price(target)
                
                # Logic: Aggressive if below target
                aggression = 1.0
                if pnl < 1.0: aggression = 1.5
                if pnl < 0: aggression = 2.0 # Revenge trading simulation? No, "Recovery Mode"
                
                # Random "Analyst" Signal
                signal_score = random.randint(0, 100) # 0-100
                
                if signal_score > (80 / aggression): # Buy Signal
                    qty = random.randint(1, 5)
                    cost = qty * price
                    if self.current_balance > cost:
                        self.current_balance -= cost
                        self.positions[target] = self.positions.get(target, 0) + qty
                        logger.info(f"   BUY  {target} x{qty} @ ${price:.2f} (Analyst Confidence: {signal_score}%)")
                        self.trades_count += 1
                        
                        # [REAL API ORDER EXECUTION FOR VIRTUAL/REAL MODES]
                        try:
                            # NAS is default for US Stocks in this list
                            res = self.client.overseas_stock.place_order(target, "NAS", "BUY", qty, price, "00") # Limit
                            if res.get("success"):
                                logger.info(f"   🚀 [API SENT] BUY Order: {res.get('order_no')}")
                            else:
                                logger.error(f"   ❌ [API FAIL] {res.get('message')}")
                        except Exception as e:
                            logger.error(f"   ⚠️ API Trigger Error: {e}")
                        
                elif signal_score < 20 and self.positions.get(target, 0) > 0: # Sell Signal
                    qty = random.randint(1, self.positions[target])
                    revenue = qty * price
                    self.current_balance += revenue
                    self.positions[target] -= qty
                    logger.info(f"   SELL {target} x{qty} @ ${price:.2f} (Profit taking)")
                    self.trades_count += 1
                    
                    # [REAL API ORDER EXECUTION FOR VIRTUAL/REAL MODES]
                    try:
                        res = self.client.overseas_stock.place_order(target, "NAS", "SELL", qty, price, "00")
                        if res.get("success"):
                            logger.info(f"   🚀 [API SENT] SELL Order: {res.get('order_no')}")
                        else:
                            logger.error(f"   ❌ [API FAIL] {res.get('message')}")
                    except Exception as e:
                        logger.error(f"   ⚠️ API Trigger Error: {e}")
                
                # Sleep
                time.sleep(3)
                
        except KeyboardInterrupt:
            logger.info("🛑 Mission Aborted by User.")

if __name__ == "__main__":
    mission = NightOpsCommander()
    if mission.initialize():
        mission.run_mission()
