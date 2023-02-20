import yfinance as yf
import pandas as pd
import datetime as dt

def stock_to_csv():

    stocks = ['AAPL','MSFT','AMZN','TSLA','GOOGL']

    for stock in stocks:

        stock_ticker = yf.Ticker(stock)

        stock_data = stock_ticker.history(period='1y')

        stock_data.reset_index(inplace=True)

        stock_df = pd.DataFrame(stock_data)

        stock_df['Date'] = stock_df['Date'].dt.date

        #print(stock_df.head())
        
        #print(stock_df.dtypes)

        stock_df.to_csv('/Users/carlosolivella/Desktop/web_class/group_project/csv_files/' + stock + '.csv', index=False)

stock_to_csv()
