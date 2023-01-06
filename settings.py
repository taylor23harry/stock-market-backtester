class Settings:
    """Contains all settings attributes."""
    def __init__(self):
        # RSI200MA
        self.historical_path = 'E:/Programming/Stock market bot/data/historical/'
        self.rsi_time_window = 8
        self.timeframe = 2000 # Timeframe for how much data is downloaded
        
        # Trading Bot
        self.capital = 1000
        self.stock_start_date = '2011-06-22'