import os
import shutil
from datetime import date, datetime,  timedelta
from statistics import mean
import pandas as pd
import numpy as np
import yfinance as yf
import glob
import csv
from settings import Settings

class RSI200MA:
    """Buys stocks when current price is under 200MA and RSI10<30, sells when RSI10>40."""

    def __init__(self):
        """Initialises all external attributes."""
        self.settings = Settings()

    def main(self):
        """Contains launchers to all used methods."""
        #r1.data_download(stocks_csv, self.settings.timeframe)
        r1.rsi()
        r1.MA()

    def data_download(self, file, timeframe=2000):
        """Downloads stock data from Yahoo Finance."""
        self.timeframe = timeframe + ((timeframe / 7)*5)
        # Reads CSV file containing relevant stock names
        df = pd.read_csv(file)
        # Store the names of stocks in a 'stocks' list
        self.stocks = df['Stock_name'].tolist()
        # Fetches current time and stores it
        self.today = date.today()
        self.end = self.today.strftime("%Y-%m-%d")
        self.start = self.today-timedelta(self.timeframe+1)
        self.time_path = 'E:/Programming/Stock market bot/time/'

        def delete_data():
            """Deletes historical data."""
            try:
                os.mkdir(self.settings.historical_path)
            except FileExistsError:
                pass
            shutil.rmtree(self.settings.historical_path)
            os.mkdir(self.settings.historical_path)

        def download():
            """Downloads new data from Yahoo! Finance."""
            for stock in self.stocks:
                temp = yf.download(stock, self.start, self.end, rounding=True)
                d1 = pd.DataFrame(temp)
                pd.DataFrame.to_csv(temp, f'{self.settings.historical_path}{stock}.csv')


        # Decides if it's necessary to download new data
        downloaded = False
        try:
            with open(f'{self.time_path}time.txt', 'r') as dayfile:
                day = dayfile.read()
                print(day, self.today)
        except FileNotFoundError:
            print("time.txt file not found. Creating one now and downloading data.")
            # Deletes old data.
            delete_data()
            # Downloads data if time.txt doesn't exist and create time.txt*
            download()
            downloaded = True
            with open(f'{self.time_path}time.txt', 'w') as dayfile:
                dayfile.write(str(self.today))
            day = str(self.today)
            
        if day != str(self.today):
            # Deletes old data.
            delete_data()
            # Downloads stock data and stores data seperately in CSV
            download()
            downloaded = True
            # Updates time.txt
            with open(f'{self.time_path}time.txt', 'w') as dayfile:
                dayfile.write(str(self.today))
            
        if not downloaded:
            print("Current data still relevant. No need to re-download.")

    def ema(self, data, period):
        ema_dataframe = pd.DataFrame(data)
        return ema_dataframe.ewm(span=period)



    def rsi(self):
        """Calculates 10 day Relative Strength Index for each stock."""
        stock_paths = (glob.glob(f"{self.settings.historical_path}*"))
        
        for stock in stock_paths:
            data = pd.read_csv(stock)
            df = pd.DataFrame(data)
            company_name = ((os.path.basename(stock)).split(".csv")[0])

            def computeRSI (data, time_window=10):
                diff = data.diff(1).dropna()        # diff in one field(one day)

                #this preservers dimensions off diff values
                up_chg = 0 * diff
                down_chg = 0 * diff
    
                # up change is equal to the positive difference, otherwise equal to zero
                up_chg[diff > 0] = diff[ diff>0 ]
    
                # down change is equal to negative deifference, otherwise equal to zero
                down_chg[diff < 0] = diff[ diff < 0 ]
    
                            # check pandas documentation for ewm
                # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
                # values are related to exponential decay
                # we set com=time_window-1 so we get decay alpha=1/time_window
                up_chg_avg   = up_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
                down_chg_avg = down_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
                
                rs = abs(up_chg_avg/down_chg_avg)
                rsi = 100 - 100/(1+rs)
                return rsi



            df['RSI'] = computeRSI(df['Close'], self.settings.rsi_time_window)
            pd.DataFrame.to_csv(df, stock)

    def MA(self, timeframe=200):
        """Calcuates Moving Average for each stock."""
        stock_paths = (glob.glob(f"{self.settings.historical_path}*"))
        
        for stock in stock_paths:
            data = pd.read_csv(stock)
            df = pd.DataFrame(data)
            company_name = ((os.path.basename(stock)).split(".csv")[0])

            def moving_average(data, timeframe=200):
                #cumsum = np.cumsum(np.insert(data, 0, 0))
                #return (cumsum[timeframe:] - cumsum[:-timeframe] / float(timeframe))
                return data.rolling(window=200).mean()
                
            
            df['200MA'] = moving_average(data['Close'])

            pd.DataFrame.to_csv(df, stock)


                    





if __name__ == '__main__':
    stocks_csv = 'E:/Programming/Stock market bot/data/stocks.csv'
    r1 = RSI200MA()
    r1.main()