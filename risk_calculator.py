## Setup 

capital = input("What's your current capital? : ")

shares_number = input("How many shares? : ")
direction = input("Are you short or long? : ")
share_price = input("What's the average fill price for each share? : ")

stop_loss = input("Where is your stop-loss? : ")
take_profit = input("Where is your take-profit? : ")

risk_per_trade = 2 # In % of your total capital

# Calculation

risk_per_trade = (capital * (risk_per_trade/100))
risk = (share_price - stop_loss) * shares_number
shares_number = 

if direction == "Long" or "long":
    

elif direction == "Short" or "short":
    pass
