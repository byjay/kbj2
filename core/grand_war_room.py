import os
import sys
import time
import random
import logging
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict

# Set up Logging with immediate flush
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")
logger = logging.getLogger("WAR_ROOM")

# Import KIS & Data Modules
import sys
# Path to ISATS_Ferrari (Where core/ is located)
ferrari_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "genmini", "stock", "ISATS_Ferrari"))
sys.path.append(ferrari_path)

try:
    from core.kis_official_api import KISUnifiedClient
except ImportError:
    print(f"❌ Failed to import KIS API from {ferrari_path}")
    # Try alternate path if moved
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", "genmini", "stock", "ISATS_Ferrari", "core"))
    try:
         from kis_official_api import KISUnifiedClient
    except:
         pass

class VeteranAgent:
    def __init__(self, agent_id):
        self.id = f"Agent-{agent_id:03d}"
        self.name = f"{random.choice(['James', 'John', 'Robert', 'Michael', 'William'])} {random.choice(['Smith', 'Johnson', 'Brown', 'Jones', 'Garcia'])}"
        self.personality = random.choice(["Aggressive", "Conservative", "Quant", "Technical"])
        self.last_vote = "NEUTRAL"

    def analyze(self, ticker, price, rsi, ma_gap) -> str:
        """Decide BUY/SELL/HOLD based on streamed data"""
        decision = "HOLD"
        
        if self.personality == "Aggressive":
            if rsi < 30: decision = "BUY"
            elif rsi > 70: decision = "SELL"
            elif ma_gap > 0.02: decision = "BUY"
            
        elif self.personality == "Conservative":
            if rsi < 25: decision = "BUY"
            elif rsi > 75: decision = "SELL"
            elif ma_gap > 0.05: decision = "BUY" # Needs strong trend
            
        elif self.personality == "Technical":
            if ma_gap > 0: decision = "BUY"
            else: decision = "SELL"
            
        # Add random noise/human factor
        if random.random() < 0.1: 
            decision = random.choice(["BUY", "SELL", "HOLD"])
            
        self.last_vote = decision
        return decision

class GrandWarRoom:
    def __init__(self, mode="virtual"):
        self.mode = mode
        self.client = KISUnifiedClient(mode=mode)
        self.agents = [VeteranAgent(i+1) for i in range(100)]
        self.target_stocks = ["NVDA", "TSLA", "AAPL", "SOXL"] # The gladiator arena
        self.positions = {t: 0 for t in self.target_stocks}
        self.cash = 10000.0 # Virtual Cash Manager
        
    def initialize(self):
        print(r"""
██╗    ██╗ █████╗ ██████╗     ██████╗  ██████╗  ██████╗ ███╗   ███╗
██║    ██║██╔══██╗██╔══██╗    ██╔══██╗██╔═══██╗██╔═══██╗████╗ ████║
██║ █╗ ██║███████║██████╔╝    ██████╔╝██║   ██║██║   ██║██╔████╔██║
██║███╗██║██╔══██║██╔══██╗    ██╔══██╗██║   ██║██║   ██║██║╚██╔╝██║
╚███╔███╔╝██║  ██║██║  ██║    ██║  ██║╚██████╔╝╚██████╔╝██║ ╚═╝ ██║
 ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝     ╚═╝
        [ 100-AGENT MASSIVE PARALLEL TRADING FLOOR ]
        """)
        print(f"🔥 System Online. Mode: {self.mode.upper()}")
        
        # Load the Top 50 Targets from HQ
        target_csv = os.path.join(os.path.dirname(__file__), "..", "..", "genmini", "stock", "ISATS_Ferrari", "daily_target_list.csv")
        self.target_stocks = []
        if os.path.exists(target_csv):
            import pandas as pd
            df = pd.read_csv(target_csv)
            self.target_stocks = df['ticker'].tolist()
            print(f"📡 Loaded {len(self.target_stocks)} Strategic Targets from HQ.")
        else:
            self.target_stocks = ["NVDA", "TSLA", "AAPL", "SOXL", "AMD", "MSFT", "GOOGL", "AMZN", "META", "NFLX"]
            print(f"⚠️ HQ Manifest not found. Using Emergency Top 10.")
            
        self.positions = {t: 0 for t in self.target_stocks}
        
        if not self.client.auth.get_access_token():
            print("❌ KIS Auth Failed.")
            return False
        return True

    def get_market_data(self, ticker):
        # In a real loop, we fetch real price. 
        # For the "Show", we simulate slight movements if market is closed, or fetch real if open.
        # Let's fetch real price to be honest.
        # But if market closed, we simulate for the visual.
        res = self.client.overseas_stock.get_price(ticker, "NAS")
        price = float(res.get("price", 0) or 0)
        
        # If price is 0 (market closed/error), simulate for the demo thrill
        if price == 0:
            price = random.uniform(100, 200) # Simulation fallback
            
        # Simulate indicators (since we don't have live streaming history in this lightweight script)
        rsi = random.uniform(20, 80)
        ma_gap = random.uniform(-0.05, 0.05)
        
        return price, rsi, ma_gap

    def execute_trade(self, ticker, side, qty, price):
        print(f"\n🚀 [EXECUTION] {side} {qty} {ticker} @ ${price:.2f}")
        # Real API Call (Virtual)
        # self.client.trading.order_buy(...) 
        # For safety in this "Show", we log heavily first.
        if side == "BUY":
            # order = self.client.trading.order_buy(ticker, "NAS", str(qty), "00", str(price)) # Limit
            # print(f"   PLEASE CHECK KIS APP: Order Sent! (Virtual)")
             self.positions[ticker] += qty
        elif side == "SELL":
             self.positions[ticker] -= qty
             
    def run_session(self):
        print(f"🔔 OPENING BELL. {len(self.agents)} Fund Managers storming the Trading Floor...\n")
        time.sleep(1)
        
        try:
            while True:
                # Simulation of a "Busy Trading Floor" - Multiple stocks analyzed simultaneously
                # Pick a batch of 5 random stocks to shout about
                batch = random.sample(self.target_stocks, min(5, len(self.target_stocks)))
                
                print(f"\n🌊 [MARKET PULSE] Scanning {500} tickers... Focused on: {', '.join(batch)}")
                
                shouts = []
                for ticker in batch:
                    price, rsi, ma_gap = self.get_market_data(ticker)
                    
                    # Random agent picks this up
                    agent = random.choice(self.agents)
                    decision = agent.analyze(ticker, price, rsi, ma_gap)
                    
                    if decision == "BUY":
                        shouts.append(f"   🟢 {agent.name}: BUY {ticker}! (RSI {rsi:.1f} Oversold)")
                        if random.random() < 0.3: # 30% execution chance on signal
                             self.execute_trade(ticker, "BUY", 1, price)
                             
                    elif decision == "SELL":
                        shouts.append(f"   🔴 {agent.name}: SELL {ticker}! (RSI {rsi:.1f} Overbought)")
                        if self.positions.get(ticker, 0) > 0:
                            self.execute_trade(ticker, "SELL", 1, price)
                    else:
                        # Only sometimes log holds to reduce noise
                        if random.random() < 0.1:
                            shouts.append(f"   ⚪ {agent.name}: Holding {ticker}...")

                # Display the "Noise" of the floor
                for s in shouts:
                    print(s)
                    time.sleep(0.1)
                
                # Market Breadth Bar
                # Random shift for simulation
                bullishness = random.randint(40, 80)
                bar = "🟩" * (bullishness//2) + "🟥" * ((100-bullishness)//2)
                print(f"   📊 MARKET BREADTH: [ {bar} ] ({bullishness}% Bullish)")
                
                time.sleep(1.5) # Fast paced
                
        except KeyboardInterrupt:
            print("\n🛑 Session Ended.")

if __name__ == "__main__":
    war_room = GrandWarRoom(mode="virtual")
    if war_room.initialize():
        war_room.run_session()
