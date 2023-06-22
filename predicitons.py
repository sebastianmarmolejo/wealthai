import pandas as pd
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from stocks_sample import stock_symbols_sample



# Fetch stock data for a given symbol
def fetch_stock_data(stock_symbol, start_date, end_date):
    try:
        stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
        return stock_data
    except Exception as e:
        print(f"Error fetching data for symbol {stock_symbol}: {str(e)}")
        return None

# Train and evaluate a Random Forest regressor for stock price prediction
def train_and_evaluate(symbol, start_date, end_date):
    # Fetch stock data
    stock_data = fetch_stock_data(symbol, start_date, end_date)

    if stock_data is None:
        return None

    # Prepare the data for training
    X = stock_data.drop(columns=['Close'])
    y = stock_data['Close']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a Random Forest regressor
    regressor = RandomForestRegressor(random_state=42)
    regressor.fit(X_train, y_train)

    # Evaluate the model
    y_pred = regressor.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)

    return regressor, mae

def get_predictions(stock_symbols, start_date, end_date):
    # Perform stock price prediction for each symbol
    predictions = []

    for symbol in stock_symbols:
        model, mae = train_and_evaluate(symbol,start_date, end_date)

        if model is not None:
            prediction = {'Symbol': symbol, 'Model': model, 'MAE': mae}
            predictions.append(prediction)

    # Sort the predictions based on MAE (mean absolute error)
    predictions.sort(key=lambda x: x['MAE'])

    # Fetch stock data for the best symbol
    best_symbol = predictions[0]['Symbol']
    best_stock_data = fetch_stock_data(best_symbol, start_date, end_date)

    if best_stock_data is not None:
        # Create an empty DataFrame to store the predictions
        df_predictions = pd.DataFrame(columns=['Date', 'Symbol', 'Actual Close', 'Predicted Close'])

        # Iterate through each prediction
        for prediction in predictions:
            symbol = prediction['Symbol']
            model = prediction['Model']

            # Fetch stock data for the symbol
            stock_data = fetch_stock_data(symbol, start_date, end_date)

            if stock_data is not None:
                # Make predictions using the model
                predicted_prices = model.predict(stock_data.drop(columns=['Close']))

                # Add the actual and predicted prices to the DataFrame
                predictions_data = pd.DataFrame({'Date': stock_data.index, 'Symbol': symbol,
                                                'Actual Close': stock_data['Close'], 'Predicted Close': predicted_prices})
                df_predictions = pd.concat([df_predictions, predictions_data], ignore_index=True)

        # Save predictions to CSV
        df_predictions.to_csv('stock_predictions.csv', index=False)


# # Define the stock symbols and date range
# stock_symbols = stock_symbols_sample
# start_date = '2023-01-01'
# end_date = '2023-04-30'

# result = get_predictions(stock_symbols,start_date, end_date)
