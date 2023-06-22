import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def visualize_stock_predictions(symbols,end_date):
    df_predictions = pd.read_csv('stock_predictions.csv')

    # Convert the 'Date' column to datetime format
    df_predictions['Date'] = pd.to_datetime(df_predictions['Date'])

    # Filter the data for the specified symbols and end date
    filtered_data = df_predictions[df_predictions['Symbol'].isin(symbols) & (df_predictions['Date'] <= end_date)]
    predicted_data = df_predictions[df_predictions['Symbol'].isin(symbols) & (df_predictions['Date'] > end_date)]

     # Set the dark theme style
    plt.style.use('dark_background')

    # Plotting the actual prices
    plt.figure(figsize=(10, 6))
    for symbol in symbols:
        symbol_data = filtered_data[filtered_data['Symbol'] == symbol]
        plt.plot(symbol_data['Date'], symbol_data['Actual Close'], label=f'Actual Close ({symbol})')

    # Plotting the predicted prices
    for symbol in symbols:
        symbol_data = predicted_data[predicted_data['Symbol'] == symbol]
        plt.plot(symbol_data['Date'], symbol_data['Predicted Close'], label=f'Predicted Close ({symbol})')

    # Set the plot title and labels
    plt.title('Stock Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')

    # Adjust x-axis labels
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # Format as "Jan 2023"

    # Set the limits of the x-axis
    plt.xlim(df_predictions['Date'].min(), df_predictions['Date'].max())

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45)

    # Move the legend to the top-right corner
    plt.legend(loc='upper left')

    # Display the plot
    plt.tight_layout()
    # plt.show()
    return plt


