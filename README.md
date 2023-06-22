# ML-Powered Investment Advisor

This is a Streamlit app that serves as an ML-powered investment advisor. It provides investment recommendations based on machine learning models trained on historical financial data.

This project was develped in a few weeks as an MVP for my Fintech course at university.

## Prerequisites

Before running the application, ensure that you have the following prerequisites installed:

- Python (version 3.6 or higher)
- Required Python libraries (specified in `app.py`)

## Installation

1. Clone this repository to your local machine or download and extract the ZIP file.

2. Open a terminal or command prompt and navigate to the project directory.

3. Install the packages specified on requirements.txt


## Usage

To run  app, follow these steps:

1. Open a terminal or command prompt, or run the code on your favorite code editor.

2. Navigate to the project directory.

3. Run the `app.py` script using Python:

4. Once the application is running, a URL will be displayed in the terminal. Open that URL in your web browser.

5. You will be presented with the Streamlit app interface, where you can interact with the ML-powered investment advisor.

6. Follow the on-screen instructions to provide the necessary inputs and receive investment recommendations based on the ML models.

7. When you're done, you can stop the application by pressing `Ctrl+C` in the terminal or command prompt.

8. A sample of stocks is specified on stocks_sample.py, you may change this sample to any stocks you'd like to see.

9. You may specify a different time parameter for the analysis and prediciton as well changing the parameters on the app.py

10. The app wil by default use the existing data, change line 25 to get new data, though this might take a while since it needs to run all the data processing

## Features

Each of the app features has its own script, they are defined as functions and implemented on the app. The app MVP contains the following functioning features:

1. A risk categorizer that uses volatility analysis for defining the risk profile of a stock

2. A trend analysis that provides recommendations for buying, selling, or holding stocks

2. A Machine Learning prediction that draws a forecast for each month with the given period



