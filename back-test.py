from datetime import date, datetime, timedelta
import pandas as pd
import numpy as np
import glob
import os
from settings import Settings

class BackTest:
    """Main backtest class."""
    def __init__(self):
        self.settings = Settings()


    def main(self):
        """Contains all necessary methods and functions to perform backtest."""
        stock_paths = glob.glob(f"{self.settings.historical_path}*")
        balance = self.settings.capital
        equity = balance

        ## Filters out all stock is current price < 20
        usable_stocks = stock_paths.copy()
        #print(stock_paths)
        for i in range(3):
            for stock in stock_paths:
                data = pd.read_csv(stock)
                df = pd.DataFrame(data)
                self.total_days = df['Date'].to_list()
                company_name = ((os.path.basename(stock)).split(".csv")[0])
                
                #print(f"{company_name} Start Date : {self.total_days[0]}")
                if self.total_days[0] != '2011-06-22':
                    #print(f"Deleted {company_name} because their start date is {self.total_days[0]}")
                    del stock_paths[stock_paths.index(stock)]
                
        #stock_paths = [stock for stock in usable_stocks if pd.DataFrame(pd.read_csv(stock))['Date'].to_list()[0] == '2011-06-22']

        # Gets correct date
        for stock in stock_paths:
            data = pd.read_csv(stock)
            df = pd.DataFrame(data)
            self.total_days = df['Date'].to_list()
            break



        print(stock_paths)            
        # Logging system
        log = pd.DataFrame(columns=['Trade', 'Date', 'Stock', 'Amount', 'Buy', 'Sell', 'Stop Loss', 'Profit', 'Profit %', 'Equity', 'Sell Date'])
        trade_id = 0

        ## For each day, find relevant stocks
        total_timeframe = [i for i in range(int(len(self.total_days)))]
        for day in total_timeframe[200:2365]:
            print(f"\n\t{total_timeframe.index(day)}")
            usable_stocks = [] # Relevant stocks
            for stock in stock_paths:
                data = pd.read_csv(stock)
                df = pd.DataFrame(data)
                RSIs = []
                MAs = []
                Closing = []
                RSIs = df['RSI'].to_list()
                MAs = df['200MA'].to_list()
                Closing = df['Adj Close'].to_list()
                days = df['Date'].to_list()
                company_name = ((os.path.basename(stock)).split(".csv")[0])

                
                # Adds stock to relevant stocks if 
                # current price is > 200MA
                # and RSI(10) < 30

                if Closing[day] > MAs[day] and RSIs[day] < 30:
                    usable_stocks.append(stock)
            print(self.total_days[day])

            ## Calculates how much of your balance you can spend on each stock.
            if len(usable_stocks) != 0:
                budget_per_stock = balance / len(usable_stocks)
                bought_stocks = []

                for stock in usable_stocks:
                    data = pd.read_csv(stock)
                    df = pd.DataFrame(data)
                    Closing = []
                    Closing = df['Adj Close'].to_list()
                    days = df['Date'].to_list()

                    if Closing[day] <= budget_per_stock:
                        bought_stocks.append(stock)

                portfolio_df = pd.DataFrame(columns=['Trade', 'Stock', 'Amount'])

                for stock in bought_stocks:
                    data = pd.read_csv(stock)
                    df = pd.DataFrame(data)
                    Closing = []
                    Closing = df['Adj Close'].to_list()
                    Opening = df['Open'].to_list()
                    days = df['Date'].to_list()      
                    company_name = ((os.path.basename(stock)).split(".csv")[0]) 


                    # Buy amount_of_stocks
                    amount_of_stocks = int(budget_per_stock / Opening[day+1])
                    if amount_of_stocks != 0:
                        trade_id += 1
                        balance -= Opening[day+1] * amount_of_stocks
                        stop_loss = Opening[day+1] - (Opening[day+1]*0.04)
                        trade = {'Trade': trade_id, 'Date': days[day], 'Stock': company_name, 'Stop Loss': stop_loss, 'Amount': amount_of_stocks, 'Buy': Opening[day+1]}
                        log = log.append(trade, ignore_index=True)
                        

                        print(f"\tBought {amount_of_stocks} of {company_name} @ {Opening[day+1]}. \t\tNew balance : {balance}, Stop Loss : {stop_loss}")
                        
                        # Saves portfolio
                        portfolio_row = {'Trade': trade_id, 'Stock': company_name, 'Amount': amount_of_stocks}
                        portfolio_df = portfolio_df.append(portfolio_row, ignore_index=True)

                #portfolio_df = pd.DataFrame({'Trade': trade_ids, 'Stock':owned_stocks,'Amount':amount_of_stocks_owned}, columns=['Stock', 'Amount'])
                #portfolio_df['Stock'] = owned_stocks
                #portfolio_df['Amount'] = amount_of_stocks_owned

            pd.DataFrame.to_csv(portfolio_df, 'E:/Programming/Stock market bot/portfolio/portfolio.csv') 
            pd.DataFrame.to_csv(log, 'E:/Programming/Stock market bot/log/log.csv')


            # Loads Log data
            log_data = pd.read_csv('E:/Programming/Stock market bot/log/log.csv')
            log = pd.DataFrame(log_data)

            # Loads portfolio data
            portfolio = pd.read_csv('E:/Programming/Stock market bot/portfolio/portfolio.csv')
            portfolio_df = pd.DataFrame(portfolio)
            company_names = portfolio_df['Stock'].to_list()
            amounts = portfolio_df['Amount'].to_list()
            
            logged_trade_ids = log['Trade'].to_list()
            logged_stock_names = log['Stock'].to_list()
            logged_amounts = log['Amount'].to_list()
            logged_buy_prices = log['Buy'].to_list()
            logged_stop_losses = log['Stop Loss'].to_list()

            Closing = df['Adj Close'].to_list()
            Non_adj_close = df['Close'].to_list()
            Opening = df['Open'].to_list()
            days = df['Date'].to_list()  
            RSIs = df['RSI'].to_list()
            
            #for company_name in company_names:
            for trade in logged_trade_ids:

                trade_id = logged_trade_ids.index(trade)
                company_name = logged_stock_names[trade_id]
                stock_path = f"E:/Programming/Stock market bot/data/historical/{company_name}.csv"

                # Fetches traded stock data
                data = pd.read_csv(stock_path)
                df = pd.DataFrame(data)
                Closing = df['Adj Close'].to_list()
                Opening = df['Open'].to_list()


                sell_price = Opening[day+1]
                bought_price = logged_buy_prices[trade_id]
                if company_name != 'nan':
                    stock_path = f'{self.settings.historical_path}{company_name}.csv'
                    data = pd.read_csv(stock_path)
                    df = pd.DataFrame(data)
                    buy_price = logged_buy_prices[trade_id]

                    amount_of_stocks = logged_amounts[trade_id]
                    log.loc[log.Trade == trade, 'Sell'] = sell_price


                    # Sells if RSI > 70 or 4% loss
                    stop_loss = logged_stop_losses[trade_id]
                    
                    if RSIs[day] > 70 or Non_adj_close[day] < stop_loss:
                        balance += sell_price * amount_of_stocks
    
                        # Calculates profit difference, profit percentage and equity
                        difference = (sell_price * amount_of_stocks) - (bought_price * amount_of_stocks)
                        equity += difference
                        profit_percentage = ((sell_price * amount_of_stocks) / (bought_price * amount_of_stocks))*100-100
                        
                        # Updates log
                        log.loc[log.Stock == company_name, 'Profit'] = difference
                        log.loc[log.Stock == company_name, 'Equity'] = equity
                        log.loc[log.Stock == company_name, 'Profit %'] = profit_percentage
                        log.loc[log.Stock == company_name, 'Sell Date'] = days[day]

                        print(f"\tSold {amount_of_stocks} of {company_name} @ {sell_price}. \t\tNew balance : {balance}, Stop loss : {stop_loss} : Equity {equity}")

                        """try:
                            portfolio_df = portfolio_df.drop(logged_trade_ids.index(trade_id))
                            portfolio_df.loc[portfolio_df.Trade == trade_id, "Stock"] = None
                            portfolio_df.loc[portfolio_df.Trade == trade_id, "Amount"] = None
                            portfolio_df.loc[portfolio_df.Trade == trade_id, "Trade"] = None
                        except KeyError:
                            print(f"KeyError whilst removing trade : {trade_id} from portfolio")
                        except ValueError:
                            print(f"ValueError whilst removing trade : {trade_id} from portfolio")"""
                            
            
            #portfolio_df['Stock'] = company_names
            #portfolio_df['Amount'] = amounts            
            pd.DataFrame.to_csv(portfolio_df, 'E:/Programming/Stock market bot/portfolio/portfolio.csv')
            pd.DataFrame.to_csv(log, 'E:/Programming/Stock market bot/log/log.csv')

            


        

if __name__ == '__main__':
    b = BackTest()
    b.main()