## A script to fetch appropriate stocks according to RSI > 30 and Last > 200MA
## I'm using the VSCode extension "Better Comments", so when you see //* and */
## everywhere, that's why.
from datetime import date
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

file = 'E:\\Programming\\Stock market bot\\data\\stocks.csv'

with webdriver.Firefox() as driver:
    driver.get('https://www.tradingview.com/screener/')
    time.sleep(5)
    driver.find_element_by_xpath('/html/body/div[7]/div/div[2]/div[13]').click()

    # Search
    search = driver.find_element_by_xpath("/html/body/div[13]/div/div/div/div[2]/input")
    search.send_keys("Relative Strength Index")
    time.sleep(3)
    # Filters RSI
    RSI = driver.find_element_by_xpath('/html/body/div[13]/div/div/div/div[3]/div[1]/div/div/div[122]/div[2]/input[1]')
    #driver.execute_script("arguments[0].click();", RSI)
    RSI.send_keys("30")
    time.sleep(1)
    RSI7 = driver.find_element_by_xpath('/html/body/div[13]/div/div/div/div[3]/div[1]/div/div/div[123]/div[2]/input[1]')
    RSI7.send_keys("30")
    time.sleep(1)
    # Filters SMA 200
    for letter in "Relative Strength Index":
        search.send_keys(Keys.BACKSPACE)
    search.send_keys("Simple Moving Average")
    time.sleep(2)
    # Selects then switches to SMA 200 filter
    SMA200 = driver.find_element_by_xpath('/html/body/div[13]/div/div/div/div[3]/div[1]/div/div/div[133]/div[2]/label[2]/span/span')
    SMA200.click()
    time.sleep(1)
    # Choses option 'Last' in dropdown
    driver.find_element_by_xpath('/html/body/div[13]/div/div/div/div[4]/div/div[1]/span[5]/span').click()
    time.sleep(1)
    # Closes filter screen
    driver.find_element_by_xpath('/html/body/div[13]/div/div/div/div[1]/div[4]').click()
    time.sleep(1)
    # Find stocks
    stocks = driver.find_elements_by_xpath('/html/body/div[7]/div/div[4]/table/tbody/tr[*]')
    
    today = date.today()
    today = today.strftime("%B %d, %Y")

#
# Prints out relevant stocks to CSV.
#
#    *! WARNING !! the old_stocks and to_be_added lists are used interchangibly in the following section
#    *! to avoid issues related to editing a list you are currently looping through.
#*/
    banned = ['NASDAQ:WMGI', 'NASDAQ:EVOK', 'NASDAQ:ADM']

    with open(file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        old_stocks = [row for row in reader]
        print(f"{old_stocks}\n --------------------------------\n")

        with open(file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Writes header
            writer.writerow(['Stock_name', 'Date_added'])
            # Stores stock data received from webscraper
            new_stocks = []
            for stock in stocks:
                name = stock.get_attribute("data-symbol")    
                if name not in banned:
                    new_stocks.append(name)
            to_be_added = []
            # If CSV is empty, skip filtering and paste all webscraped results to CSV
            if len(old_stocks) == 0:
                for name in new_stocks:
                    writer.writerow([name, today])
            else:
                # Removes irrelevant, old stocks.
                to_be_added = [stock for stock in old_stocks if stock[0] in new_stocks]
                # Adds new stocks
                to_add = [stock[0] for stock in to_be_added]
                for stock in new_stocks:
                    if stock not in to_add:
                        print(f"Added new stock : {stock}")
                        to_be_added.append([stock, today])
                print(f"\n{to_be_added}")
                old_stocks = to_be_added.copy()

                # Remove duplicates 
                deleted = False
                temp = []
                for stock in old_stocks:
                    if stock[0] not in temp:
                        temp.append(stock)
                    else:
                        print(f"Deleted duplicate : {stock}")
                        del to_be_added[stock]
                        deleted = True
                if deleted:
                    print(f"\n\nAfter deleting duplicates {to_be_added}")
                    
                # Prints results to CSV.
                for stock in to_be_added:
                    writer.writerow([stock[0], stock[1]])
                    
                    
    with open(file, 'r') as file_object:
        content = file_object.read()
    with open(file, 'w') as file_object:
        content = content.replace('NASDAQ:', '')
        content = content.replace('NYSE:', '')
        content = content.replace('NYSE ARCA:', '')
        file_object.write(content)