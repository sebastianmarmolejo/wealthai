import yfinance as yf
import pandas as pd
import numpy as np
from stocks_sample import stock_symbols_sample

def categorize_stocks_by_volatility(stock_symbols):
    # Define the time range
    start_date = "2020-01-01"
    end_date = "2021-12-31"

    risk_levels = ["Low", "Medium", "High"]
    risk_thresholds = [0.4, 0.5]  # Adjust these thresholds as per your preference

    categorized_stocks = {}

    for symbol in stock_symbols:
        # Retrieve the historical stock data
        stock_data = yf.download(symbol, start=start_date, end=end_date, progress=False)

        # Calculate the stock's volatility
        stock_data['Log Returns'] = np.log(stock_data['Close'] / stock_data['Close'].shift(1))
        stock_volatility = stock_data['Log Returns'].std() * np.sqrt(252)  # Assuming 252 trading days in a year

        # Categorize the stock based on volatility
        if stock_volatility <= risk_thresholds[0]:
            risk_level = risk_levels[0]
        elif stock_volatility <= risk_thresholds[1]:
            risk_level = risk_levels[1]
        else:
            risk_level = risk_levels[2]

        categorized_stocks[symbol] = risk_level

    # Save categorized stocks to a CSV file
    df = pd.DataFrame.from_dict(categorized_stocks, orient='index', columns=['risk_level'])
    df.index.name = 'Symbol'
    df.to_csv('categorized_stocks.csv')

    return categorized_stocks
