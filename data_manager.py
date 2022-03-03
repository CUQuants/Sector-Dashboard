import datetime as dt
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

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

#this function is meant for transaction data but for portfolio value (not return)
def stock_change_port_value(df, transaction_tuple):
    
    counter=0

    for i in df.index:
        
        if i==transaction_tuple[1]:
            break
        else:
            counter+=1
            
    df_output = df.copy()

    if transaction_tuple[2] == "buy":
        
        zeros_list=[0 for i in range(counter)]
        df_output[transaction_tuple[0]][0:counter]=zeros_list
        
    
    if transaction_tuple[2] == "sell":
        
        zeros_list=[0 for i in range(len(df_output) - counter)]
        df_output[transaction_tuple[0]][counter:len(df_output)] = zeros_list
        
    return df_output

#this function is meant for transaction data but for portfolio change (return / cumulative return) not value
def stock_change_port_return(df, transaction_tuple):

    counter = 0
    for i in df.index:
        
        if i == transaction_tuple[1]:
            break
        
        else:
            counter += 1
            
    df_output = df.copy()
    replace_value = df_output[transaction_tuple[0]][counter]
            
    if transaction_tuple[2] == "buy":
        
        replace_list = [replace_value for i in range(counter)]
        df_output[transaction_tuple[0]][0:counter] = replace_list
        
    if transaction_tuple[2] == "sell":
        
        replace_list = [replace_value for i in range(len(df_output) - counter)]
        df_output[transaction_tuple[0]][counter:len(df_output)] = replace_list
        
    return df_output

tuple_fix = ("GOOG", "2022-01-21", "sell")
port_value_df = stock_change_port_value(df, tuple_fix)   
port_return_df = stock_change_port_return(df, tuple_fix)
