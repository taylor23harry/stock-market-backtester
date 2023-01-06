import csv
import glob
import os

stock_paths = glob.glob("E:/Programming/Stock market bot/data/historical/*")
for stock in stock_paths:
    company_name = ((os.path.basename(stock)).split("_prices.csv")[0])
    with open(stock) as fr, open(f"E:/Programming/Stock market bot/data/reversed/{company_name}.csv", "w",newline='') as fw:
        cr = csv.reader(fr,delimiter=";")
        cw = csv.writer(fw,delimiter=";")
        cw.writerow(next(cr))  # write title as-is
        cw.writerows(reversed(list(cr)))
