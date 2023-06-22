import yfinance as yf
import pandas as pd
from stocks_sample import stock_symbols_sample

def get_company_info(symbols):
    data = []

    for symbol in symbols:
        # Create a Ticker object with the stock symbol
        ticker = yf.Ticker(symbol)

        # Get the company information
        info = ticker.info

        # Extract the desired information
        company_name = info.get('longName', 'N/A')
        industry = info.get('industry', 'N/A')
        sector = info.get('sector', 'N/A')
        country = info.get('country', 'N/A')

        # Store the company information in a dictionary
        company_data = {
            'Symbol': symbol,
            'Company Name': company_name,
            'Industry': industry,
            'Sector': sector,
            'Country': country
        }
        data.append(company_data)

    # Create a DataFrame to store the company information
    df = pd.DataFrame(data)
    df.to_csv('company_info.csv')

    return df

# # Example usage with multiple symbols
# symbols = stock_symbols_sample
# company_df = get_company_info(symbols)
# print(company_df)
