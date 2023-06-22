import pandas as pd

def combining_all_data():
# Read the CSV files into DataFrames
    stock_analysis_df = pd.read_csv('stock_recommendations.csv')
    categorized_stocks_df = pd.read_csv('categorized_stocks.csv')
    company_info_df = pd.read_csv('company_info.csv')

    # Merge the DataFrames based on common columns
    merged_df = pd.merge(stock_analysis_df, categorized_stocks_df, on='Symbol')
    df = pd.merge(merged_df, company_info_df, on='Symbol')

    # Arranging data
    recommendation_col = df.pop("Recommendation")
    df["Recommendation"] = recommendation_col

    recommendation_col = df.pop("risk_level")
    df["risk_level"] = recommendation_col

    cols_to_drop = ['Unnamed: 0','Country']
    df.drop(['Unnamed: 0'], axis=1, inplace=True)
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis=1)


    # Display final DataFrame
    df.to_csv('final_df.csv')
