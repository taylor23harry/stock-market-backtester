from datetime import date, datetime, timedelta
import os
import glob
import pandas as pd

#### SETUP ####
## Locates stock data and imports balance
stock_paths = glob.glob("E:/Programming/Stock market bot/data/historical/*")
balance = 100000
equity = 100000
## Filters out stocks which have a different start date to settings
usable_stocks = [stock for stock in stock_paths if pd.DataFrame(pd.read_csv(stock))['Date'].to_list()[0] == '02/01/2012']
print(usable_stocks)
## Creates a list of days in the chosen timeframe
data = pd.read_csv(usable_stocks[2])
df = pd.DataFrame(data)
total_days = df['Date'].to_list()
## Sets start and end of test
start = 200
end = 2299
## Percentage of risk per trade
risk = 0.04
# Creates log
log_path = 'E:/Programming/Stock market bot/log/log.csv'
log = pd.DataFrame(columns=['Trade', 'Date', 'Stock', 'Amount', 'Buy', 'Sell', 'Stop Loss', 'Profit',
'Profit %', 'Equity', 'Sell Date'])
pd.DataFrame.to_csv(log, log_path)
# Creates portfolio
portfolio_path = 'E:/Programming/Stock market bot/portfolio/portfolio.csv'
portfolio = pd.DataFrame(columns=['Trade', 'Stock', 'Amount'])
pd.DataFrame.to_csv(portfolio, portfolio_path)
# Trade id iterator
trade_id = 0


for stock in usable_stocks:
    data = pd.read_csv(stock)
    df = pd.DataFrame(data)
    Closing = df['Close'].to_list()
    RSIs = df['RSI'].to_list()
    MAs = df['200MA'].to_list()
    total_days

    for day in total_days:


    if Closing[day] > MAs[day] and RSIs[day] < 30 and Closing[day] > 30: