from datetime import date, datetime, timedelta
import pandas as pd
import glob
import os

"""Main back-test file to test trading strategy profitability."""

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

#### BUY / SELL FUNCTIONS ####

def buy(trade_id, stock, amount, day):
    # Reads stock data
    data = pd.read_csv(stock)
    df = pd.DataFrame(data)
    company_name = ((os.path.basename(stock)).split(".csv")[0])
    open_prices = df['Open'].to_list()
    buy_price = open_prices[day]
    # Reads Log
    log_csv = pd.read_csv(log_path, dtype={'Trade': int, 'Date': str, 'Stock': str, 'Amount': int, 'Buy': float, 'Sell': float, 'Stop Loss': float, 'Profit': float, 'Profit %': float, 'Equity': float, 'Sell Date': str})
    log = pd.DataFrame(log_csv)
    # Reads Portfolio
    portfolio_csv = pd.read_csv(portfolio_path, dtype={'Trade': int, 'Stock': str, 'Amount': int})
    portfolio = pd.DataFrame(portfolio_csv)
    # Calcualtes stop loss
    stop_loss = buy_price - (buy_price * risk)
    # Deducts price from balance
    global balance
    balance -= (buy_price * amount)
    # Log
    trade = {'Trade': trade_id, 'Date': day, 'Stock': company_name, 'Stop loss': stop_loss, 'Amount': amount, 'Buy': buy_price}
    log = log.append(trade, ignore_index=True)
    pd.DataFrame.to_csv(log, log_path)
    # Portfolio
    portfolio_trade = {'Trade': trade_id, 'Stock': company_name, 'Amount': amount}
    portfolio = portfolio.append(portfolio_trade, ignore_index=True)
    pd.DataFrame.to_csv(portfolio, portfolio_path)

    ## Print + iterate trade_id    
    print(f"\tTrade : {trade_id}; Bought {amount} x {company_name} @ {buy_price}.")
    trade_id += 1

def sell(trade_id, stock_path, day, sell_price, amount, buy_price):
    # Calcualte profit, profit percentage and equity
    profit = (sell_price * amount) - (buy_price * amount)
    profit_percentage = (sell_price * amount) / (buy_price * amount)
    equity += profit
    # Updates balance
    balance += (sell_price * amount)
    # Updates log
    log.loc[log.Trade == trade_id, 'Sell'] = sell_price
    log.loc[log.Trade == trade_id, 'Profit'] = profit
    log.loc[log.Trade == trade_id, 'Profit %'] = profit_percentage
    log.loc[log.Trade == trade_id, 'Sell Date'] = day



#### MAIN LOOP ####

for day in total_days[start:end]:
    print(f"{total_days.index(day)} : {day}")
    day_name = day
    day = total_days.index(day)

    # Finds stocks that you want to buy
    stocks_to_buy = []
    for stock in usable_stocks:
        data = pd.read_csv(stock)
        df = pd.DataFrame(data)
        Closing = df['Close'].to_list()
        RSIs = df['RSI'].to_list()
        MAs = df['200MA'].to_list()

        if Closing[day] > MAs[day] and RSIs[day] < 28 and Closing[day] > 20:
            stocks_to_buy.append(stock)

    ## Calcualtes how much of each stock you can afford
    if len(stocks_to_buy) != 0:
        budget_per_stock = balance / len(stocks_to_buy)
    
        for stock in stocks_to_buy:
            data = pd.read_csv(stock)
            df = pd.DataFrame(data)
            Closing = df['Close'].to_list()
            amount = int(budget_per_stock / Closing[day])
            
            if Closing[day] < budget_per_stock:
                # Reads stock data
                data = pd.read_csv(stock)
                df = pd.DataFrame(data)
                company_name = ((os.path.basename(stock)).split(".csv")[0])
                open_prices = df['Open'].to_list()
                buy_price = open_prices[day]
                # Reads Log
                log_csv = pd.read_csv(log_path, dtype={'Trade': int, 'Date': str, 'Stock': str, 'Amount': int, 'Buy': float, 'Sell': float, 'Stop Loss': float, 'Profit': float, 'Profit %': float, 'Equity': float, 'Sell Date': str})
                log = pd.DataFrame(log_csv)
                # Reads Portfolio
                portfolio_csv = pd.read_csv(portfolio_path, dtype={'Trade': int, 'Stock': str, 'Amount': int})
                portfolio = pd.DataFrame(portfolio_csv)
                # Calcualtes stop loss
                stop_loss = buy_price - (buy_price * risk)
                if balance - (buy_price * amount) > 0:
                    # Deducts price from balance
                    balance -= (buy_price * amount)
                    # Log
                    trade = {'Trade': trade_id, 'Date': day_name, 'Stock': company_name, 'Stop loss': stop_loss, 'Amount': amount, 'Buy': buy_price}
                    log = log.append(trade, ignore_index=True)
                    pd.DataFrame.to_csv(log, log_path)
                    # Portfolio
                    portfolio_trade = {'Trade': trade_id, 'Stock': company_name, 'Amount': amount}
                    portfolio = portfolio.append(portfolio_trade, ignore_index=True)
                    pd.DataFrame.to_csv(portfolio, portfolio_path)

                    ## Print + iterate trade_id    
                    print(f"\t\t\tTrade : {trade_id}; \tBought {amount} x \t{company_name} \t@ {buy_price}.\t Remaining balance : {balance} \tEquity : {equity}")
                    trade_id += 1

    #### Decides if you should sell stocks
    # Reads Portfolio
    portfolio_csv = pd.read_csv(portfolio_path, dtype={'Trade': int, 'Stock': str, 'Amount': int})
    portfolio = pd.DataFrame(portfolio_csv)

    bought_stocks = portfolio['Stock'].to_list()
    bought_amounts = portfolio['Amount'].to_list()
    bought_ids = portfolio['Trade'].to_list()

    ### For each stock in portfolio, check if it's time to sell
    for trade in bought_ids:
        # Reads Log
        log_csv = pd.read_csv(log_path, dtype={'Trade': int, 'Date': str, 'Stock': str, 'Amount': int, 'Buy': float, 'Sell': float, 'Stop Loss': float, 'Profit': float, 'Profit %': float, 'Equity': float, 'Sell Date': str})
        log = pd.DataFrame(log_csv)

        logged_ids = log['Trade'].to_list()
        logged_stop_losses = log['Stop Loss'].to_list()
        logged_buy_prices = log['Buy']

        stock = bought_stocks[bought_ids.index(trade)]
        amount = bought_amounts[bought_ids.index(trade)]
        stock_path = f"E:/Programming/Stock market bot/data/historical/{stock}.csv"
        buy_price = logged_buy_prices[bought_ids.index(trade)]

        # Get stock data
        data = pd.read_csv(stock_path)
        df = pd.DataFrame(data)
        Opening = df['Open'].to_list()
        Closing = df['Close'].to_list()
        RSIs = df['RSI'].to_list()
        sell_price = Opening[day+1]

        ## Check if time to sell
        if RSIs[day] <= 65 or Closing[day] < logged_stop_losses[logged_ids.index(trade)]:
            ## Sell
            #sell(trade, stock_path, day, Opening[day+1], amount, buy_price)
                # Calcualte profit, profit percentage and equity
            profit = (sell_price * amount) - (buy_price * amount)
            profit_percentage = (sell_price * amount) / (buy_price * amount)
            equity += profit
            # Updates balance
            balance += (sell_price * amount)
            # Updates log
            log.loc[log.Trade == trade, 'Sell'] = sell_price
            log.loc[log.Trade == trade, 'Profit'] = profit
            log.loc[log.Trade == trade, 'Profit %'] = profit_percentage
            log.loc[log.Trade == trade, 'Sell Date'] = day_name
            log.loc[log.Trade == trade, 'Equity'] = equity

        
            portfolio = portfolio.drop(bought_ids.index(trade))

            pd.DataFrame.to_csv(log, log_path)
            pd.DataFrame.to_csv(portfolio, portfolio_path)
    

            print(f"\t\t\tTrade : {trade}; \t Sold {amount} x \t{stock} \t@ {buy_price}.\t\t Remaining balance : {balance} \tEquity : {equity}")