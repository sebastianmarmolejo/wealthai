import pandas as pd
import yfinance as yf
from stocks_sample import stock_symbols_sample

# Fetching Stock Data
def fetch_stock_data(stock_symbol, start_date, end_date):
    try:
        stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
        return stock_data
    except Exception as e:
        print(f"Error fetching data for symbol {stock_symbol}: {str(e)}")
        return None

# Conducting trend analysis
def analyze_stock_data(stock_data):
    if stock_data is None:
        return None

    # Calculate the percentage change in stock prices
    stock_data['PriceChange'] = stock_data['Close'].pct_change()

    # Determine the trend (upward or downward)
    stock_data['Trend'] = stock_data['PriceChange'].apply(lambda x: 'Upward' if x >= 0 else 'Downward')

    # Calculate the cumulative returns
    stock_data['CumulativeReturn'] = (1 + stock_data['PriceChange']).cumprod()

    return stock_data

# Making and saving recommendations
def make_stock_recommendations(stock_symbols, start_date, end_date):
    recommendations = []

    for symbol in stock_symbols:
        # Fetch stock data
        stock_data = fetch_stock_data(symbol, start_date, end_date)

        # Analyze stock data
        analyzed_data = analyze_stock_data(stock_data)

        if analyzed_data is not None:
            # Get the last trend value and close price
            last_trend = analyzed_data['Trend'].iloc[-1]
            last_close = analyzed_data['Close'].iloc[-1]

            # Make recommendation based on the last trend
            if last_trend == 'Upward':
                recommendation = {'Symbol': symbol, 'Recommendation': 'Buy', 'Price': last_close}
            else:
                recommendation = {'Symbol': symbol, 'Recommendation': 'Sell', 'Price': last_close}

            recommendations.append(recommendation)
    
    # Save recommendations to CSV
    df_recommendations = pd.DataFrame(recommendations)
    df_recommendations.to_csv('stock_recommendations.csv', index=False)

    return recommendations

# # Define the stock symbols and date range
# stock_symbols = stock_symbols_sample
# start_date = '2022-01-01'
# end_date = '2022-12-31'

# # Make stock recommendations
# recommendations = make_stock_recommendations(stock_symbols, start_date, end_date)

# print("Stock recommendations saved to stock_recommendations.csv")
