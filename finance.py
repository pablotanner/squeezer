import yfinance as yf
import pandas as pd

def get_stock_symbols():
    # Placeholder: Replace with a comprehensive list of stock symbols
    # Here we use a small sample list for demonstration purposes
    symbols = ['NVAX', 'PLUG', 'GME', 'AMST', 'CGC']
    return symbols

def fetch_penny_stocks(symbols, start_date, end_date, threshold=5):
    penny_stocks = []
    for symbol in symbols:
        try:
            data = yf.download(symbol, start=start_date, end=end_date)
            min_price = data['Adj Close'].min()
            if min_price < threshold:
                penny_stocks.append((symbol, data))
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
    return penny_stocks

def identify_explosive_growth(penny_stocks, multiplier=10, period_days=30):
    explosive_stocks = []
    for symbol, data in penny_stocks:
        for i in range(len(data) - period_days):
            start_price = data['Adj Close'].iloc[i]
            end_price = data['Adj Close'].iloc[i + period_days]
            if start_price > 0 and end_price / start_price >= multiplier:
                explosive_stocks.append((symbol, start_price, end_price, data.index[i], data.index[i + period_days]))
                break  # If found, no need to check further for this stock
    return explosive_stocks

# Parameters
start_date = '2010-01-01'
end_date = '2023-01-01'
threshold_price = 5
multiplier = 50
period_days = 30

# Fetch stock symbols
symbols = get_stock_symbols()

# Fetch historical data and filter penny stocks
penny_stocks = fetch_penny_stocks(symbols, start_date, end_date, threshold_price)

# Identify stocks with explosive growth
explosive_growth_stocks = identify_explosive_growth(penny_stocks, multiplier, period_days)

# Display results
print("Stocks that were once penny stocks and exploded 50x in value within 30 days:")
for stock in explosive_growth_stocks:
    print(f"Symbol: {stock[0]}, Start Price: {stock[1]}, End Price: {stock[2]}, Start Date: {stock[3].date()}, End Date: {stock[4].date()}")
