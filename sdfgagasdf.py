import datetime as dt
import yfinance as yf
import pandas as pd

end = dt.date.today()
start = dt.date(end.year, 1, 1)
tickers = ["AAPL", "GOOG"]

try:
    
    df = pd.read_csv("prices.csv", index_col = 0)
    print("read from file")
    
except:
    
    df = yf.download(tickers, start, end)['Close']
    df.to_csv("prices.csv")
    print("downloaded from yahoo")
    

tuple_fix = ("GOOG", "2022-01-21")





def BuyStock(tuple_sample):
    counter=0

    for i in df.index:
        if i==tuple_fix[1]:
            break
        else:
            counter+=1


    zeros_list=[0 for i in range(counter)]
    df[tuple_fix[0]][0:counter]=zeros_list
    return df

df=BuyStock(tuple_fix)

