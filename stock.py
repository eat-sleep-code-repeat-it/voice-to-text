
# pip install yfinance
import yfinance as yf

def get_stock_price_history(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period="1d") 
    return data

def get_stock_price_market_price(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    price = ticker.info['regularMarketPrice']
    print(f"Latest price: ${price}")
    return price

#################################################
# faster, lighter, and more suitable for repeated calls
# for near-real-time price
def get_stock_price_fast_price(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    price = ticker.fast_info['last_price']
    return price
   
#############################################
#
from datetime import datetime
now = datetime.now()
current_time = now.strftime("%Y-%m-%d %H:%M:%S")

coop_price = get_stock_price_fast_price("COOP")
rkt_price = get_stock_price_fast_price("RKT")
coop_match = rkt_price * 11
profit = coop_match - coop_price
print("\n")
print("=" * 35)
print(f"{current_time}")
print("-" * 35)
print(f"{'Sell profit':<15} {(coop_price-180):>15.4f}")
print(f"{'Hold profit':<15} {profit:>15.4f}")
print(f"{'RKT':<15} {rkt_price:>15.4f}")
print(f"{'RKTx11':<15} {coop_match:>15.4f}")
print(f"{'COOP':<15} {coop_price:>15.4f}")
print("=" * 35)
