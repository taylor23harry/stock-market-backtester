from datetime import date
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


with webdriver.Firefox() as driver:
    driver.get('https://swingtradebot.com/equities?min_vol=250000&min_price=50&max_price=999999.0&adx_trend=&grade=&include_etfs=0&html_button=as_html&page=3')

    pages = driver.find_element_by_xpath('/html/body/div/div[3]/div/div[2]/div/div[4]/nav/div/div/input')
    pages = pages.get_attribute('max')
    print(pages)
    stocks = []
    next_btn = driver.find_element_by_xpath('/html/body/div/div[3]/div/div[2]/div/div[4]/nav/div/a[2]')

    time.sleep(1)
    stocks_names = driver.find_elements_by_xpath('/html/body/div/div[3]/div/div[2]/div/div[2]/table/tbody/tr[*]/td[1]/a')
    for stock_name in stocks_names:
        stocks.append(stock_name.text)
        print(stock_name.text)

