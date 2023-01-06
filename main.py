import pandas as pd
import numpy as np
import glob
from datetime import date, datetime,  timedelta
from settings import Settings
import os

class TradingBot:
    """Main trading bot class that contains the main
    algorithm."""

    def __init__(self):
        self.settings = Settings()
        self.today = date.today()

    def main(self):
        """Method that groups together all sub_methods."""
        self.data()
        self.account()
        self.actions(self.data)

    def data(self):
        """Imports all stock data."""
        self.stock_paths = glob.glob(f"{self.settings.historical_path}*")
        for stock in self.stock_paths:
            company_name = ((os.path.basename(stock)).split(".csv")[0])
            df = pd.DataFrame(stock)

    def account(self):
        """Simulates an account with a balance."""
        self.balance = self.settings.capital

    def actions(self, data):
        """Contains functions to buy and sell shares if
        certain conditions are met."""
        pass


if __name__ == '__main__':
    bot1 = TradingBot()
    bot1.main()