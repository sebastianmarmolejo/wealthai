# Importing required packages
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Importing the built functions
from visualization import visualize_stock_predictions
from risk_categorizer import categorize_stocks_by_volatility
from stock_analysis import make_stock_recommendations
from stocks_sample import stock_symbols_sample
from stock_info import get_company_info
from predicitons import get_predictions
from combining_data import combining_all_data
import warnings
warnings.filterwarnings("ignore")

# Defining the parameters for the application
stock_symbols = stock_symbols_sample
start_date = '2023-01-01'
end_date = '2023-05-31'

# Change this parameter to True to get new data
new_data = False

# Getting new data
def get_new_data(stock_symbols,start_date,end_date, new_data):
    if new_data == True:
        print('Getting new data, this might take a while...')
        # Categorizing the stocks volatility
        print('Downloading and categorizing data')
        categorize_stocks_by_volatility(stock_symbols_sample)

        # Make stock recommendations
        make_stock_recommendations(stock_symbols, start_date, end_date)

        # Getting companies' information
        get_company_info(stock_symbols_sample)

        # Making predictions for al lstocks
        get_predictions(stock_symbols,start_date, end_date)

        # Combining all the data
        combining_all_data()
    else:
        print('Using existing data')

get_new_data(stock_symbols,start_date,end_date, new_data)

# Buliling the front end
st.title("Wealth.AI")
st.markdown("AI - POWERED INVESTMENT ADVISOR")

# Creating Questionnaire
def get_risk_tolerance_level(score):
    if score >= 0 and score < 3:
        return "Low"
    elif score >= 3 and score < 6:
        return "Medium"
    elif score >= 6:
        return "High"
    else:
        return "Invalid risk tolerance value"

def risk_tolerance_questionnaire():
    st.header("Risk Profile Questionnaire")
    st.write("Please answer the following questions to assess your risk tolerance.")

    score = 0

    st.markdown("---")
    st.subheader("Question 1")
    answer1 = st.radio("Do you prefer safe and stable investments, even if they offer lower returns?", ("Yes", "No"))
    if answer1 == "Yes":
        score += 0

    st.markdown("---")
    st.subheader("Question 2")
    answer2 = st.radio("How would you feel if your investment portfolio lost 20% of its value in a short period of time?", ("Very concerned", "Somewhat concerned", "Not concerned"))
    if answer2 == "Very concerned":
        score += 0
    elif answer2 == "Somewhat concerned":
        score += 2
    elif answer2 == "Not concerned":
        score += 3

    st.markdown("---")
    st.subheader("Question 3")
    answer4 = st.radio("Are you willing to take on more risk in exchange for potentially higher returns?", ("Yes", "No"))
    if answer4 == "Yes":
        score += 3

    st.markdown("---")
    st.write("Based on your answers, your risk tolerance level is:")
    result = get_risk_tolerance_level(score)
    st.success(result)
    
    return result

risk_level = risk_tolerance_questionnaire()


# Importing the data
df = pd.read_csv('final_df.csv')

# Simulating that the user already owns some stocks
np.random.seed(123)

# Calculate the number of rows to be filled with 1
num_rows = int(10)
df['owned_stocks'] = 0
df.loc[np.random.choice(df.index, num_rows, replace=False), 'owned_stocks'] = 1

# Simulating market orders on the stocks to determine popularity
df['market_orders'] = np.random.randint(100, 5001, size=len(df))

# Getting the user's preferred industry
sector_sum = df.groupby("Sector")["owned_stocks"].sum()
preferred_sector = sector_sum.nlargest(3)

st.subheader("New Stocks")
st.write("Here are your tailored recommendations for this month, these include stocks that: ")
st.write("- Fit your risk profile based on their volatility ")
st.write("- According to our analysis are trending upwards and are at optimal buying time ")
st.write("- Popular in the industries that you like to invest in")
st.info("Select the ones you'd like to add to your order:")

# Preparing Table 1
# Excluding stocks that are already owned by the user
df_table_1 = df[df['owned_stocks'] != 1]

# Selecting only columns where the recommended analysis is to buy
df_table_1 = df_table_1[df_table_1['Recommendation'] == 'Buy']

# Selecting stocks on the user's preferred industry
df_table_1 = df_table_1[df_table_1['Sector'].isin(preferred_sector.index)]

# Selecting stocks on the user's risk_level
df_table_1 = df_table_1[df_table_1['risk_level'] == risk_level]
df_table_1.reset_index(drop=True, inplace=True)

# Selecting only the relevant columns
df_table_1 = df_table_1[['Symbol','Company Name','Sector','risk_level','market_orders']]

# Adding column for the user to select stocks
df_table_1['Add to order'] = False

# Displaying Table 1 on the front end
df_order_1 = st.data_editor(df_table_1)

# Preparing Table 2
st.subheader("Hot Stocks")
st.write("Here are some stocks that were very popular this month in industries beyond your usual preference and in all risk levels")

# Excluding stocks that are already owned by the user
df_table_2 = df[df['owned_stocks'] != 1]

# Selecting only columns where the recommended analysis is to buy
df_table_2 = df_table_2[df_table_2['Recommendation'] == 'Buy']

# Selecting stocks NOT on the user's preferred industry
df_table_2 = df_table_2[~df_table_2['Sector'].isin(preferred_sector.index)]

# Selecting only the relevant columns
df_table_2 = df_table_2[['Symbol','Company Name','Sector','risk_level','market_orders']]

# Adding column for the user to select stocks
df_table_2['Add to order'] = False

# Displaying Table on the front end
df_order_2 = st.data_editor(df_table_2)

# Combining the Data sets
df_final_order = pd.concat([df_order_1, df_order_2])
df_final_order = df_final_order[df_final_order['Add to order'] == True]
df_final_order.drop('Add to order', inplace=True, axis=1)

df_final_order = pd.merge(df_final_order, df[['Symbol', 'Price']], on='Symbol', how='left')
df_final_order["Price (in USD)"] = df_final_order['Price']
df_final_order.drop('Price', inplace=True, axis=1)
df_final_order.drop('Sector', inplace=True, axis=1)

st.subheader("AI-Powered Predictions")
st.write("Select stocks to see they performance and future predictions")

# Making the plot for the predictions
symbols_for_plot = df_final_order['Symbol']
symbols_for_plot = st.multiselect('Choose Stocks', symbols_for_plot)

viz_end_date = '2023-04-30'
plot = visualize_stock_predictions(symbols_for_plot, viz_end_date)
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot(plot)

st.subheader("Make Order")
st.write("Select the number of shares you'd like to make an order for")

df_make_order = df_final_order
df_make_order["Number of Shares"] = 0
st.data_editor(df_final_order)

st.write("Here are our recommendations for the stocks you currently own")
df_owned_stocks = df[df['owned_stocks'] == 1]
df_owned_stocks = df_owned_stocks[['Symbol', 'Company Name','risk_level','Price','Recommendation']]
df_owned_stocks["Number of Shares"] = 0
df_owned_stocks["Action"] = df_owned_stocks['Recommendation']

st.data_editor(df_owned_stocks)

if st.button('Send Purchase Order'):
    st.write('Purchase Order Sent')
    st.write('Thanks for using Wealth.AI!')
