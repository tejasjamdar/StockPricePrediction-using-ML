import yfinance as yf

stock = input("Enter the name of Stock")

sdate = input("Enter the Start date(YYYY-MM-DD)")

edate = input("Enter the End date(YYYY-MM-DD)")

data = yf.download(stock,sdate,edate)

# Get the data for the stock AAPL
#data = yf.download('GOOGL','2019-03-31','2020-04-01')
stockPrice = data['Adj Close']
print(stockPrice)

import pandas as pd

stockPrice.to_csv('historic_data.csv')

# Import the plotting library
import matplotlib.pyplot as plt
#matplotlib inline

# Plot the close price of the AAPL
data['Adj Close'].plot()
plt.show()

#import os

x = input("Press 1 to display Historic data")

if(x == 1):
    os.system('historic_data.csv')

