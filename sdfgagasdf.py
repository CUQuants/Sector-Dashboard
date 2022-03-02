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
    

tuple_fix = ("GOOG", "2022-01-21", "sell")





def stock_change(df, tuple_sample):
    counter=0

    for i in df.index:
        
        if i==tuple_sample[1]:
            break
        else:
            counter+=1

    if tuple_sample[2] == "buy":
        
        zeros_list=[0 for i in range(counter)]
        df[tuple_sample[0]][0:counter]=zeros_list
        
    
    if tuple_sample[2] == "sell":
        
        zeros_list=[0 for i in range(len(df) - counter)]
        df[tuple_sample[0]][counter:len(df)] = zeros_list
        
    return df

df=stock_change(df, tuple_fix)

