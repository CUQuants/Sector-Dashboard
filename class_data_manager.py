import pandas as pd
import yfinance as yf
import datetime as dt
import streamlit as st

class dataManager:
    
    def __init__(self, sector):
        
        self.sector = sector
        self.transactions = self.read_transactions()
        self.df_value, self.df_return = self.get_prices()
        self.df_value, self.df_return = self.complete_transactions()
        
        
    def read_transactions(self):
    
        df = pd.read_html("https://docs.google.com/spreadsheets/d/1M_alzbqePYZZPO6RQe9LmwUErNI9C6ljMlgLJmgtlG0/edit?usp=sharing")[0]
        df = df[df.columns[1:7]]
        df.columns = df.loc[0]
        df = df.drop(0)
        df = df.dropna()
        df = df[df["sector"] == self.sector]
        
        return df
        
    def get_prices(self):
    
        tickers = self.transactions["symbol"].to_list()
        end_date = dt.date.today()
        start_date = dt.date(end_date.year, 1, 1)
        df_value = yf.download(tickers, start_date, end_date)['Close']
        df_return = df_value.copy()
        
        return df_value, df_return
    
    def complete_transactions(self):
    
        check_date = pd.to_datetime(self.df_value.index[0])
        
        for i in range(len(self.transactions)):
            
            compare_date = self.transactions["date"].to_list()[i]
            compare_date = dt.datetime.strptime(compare_date,'%m/%d/%Y')
            
            if compare_date > check_date:
                
                symbol = self.transactions["symbol"].to_list()[i]
                action = self.transactions["action"].to_list()[i]
                
                transaction_tuple = (symbol, compare_date, action)
                
                self.df_value = self.stock_change_port_value(self.df_value, transaction_tuple)
                self.df_return = self.stock_change_port_return(self.df_return, transaction_tuple)
                
        return self.df_value, self.df_return
                
                
    #this function is meant for transaction data but for portfolio value (not return)
    def stock_change_port_value(self, df, transaction_tuple):
        
        counter=0
        action = transaction_tuple[2]
        action = action.lower()
    
        for i in df.index:
            
            if i==transaction_tuple[1]:
                break
            
            else:
                counter+=1
                
        df_output = df.copy()
    
        if action == "buy":
            
            zeros_list=[0 for i in range(counter)]
            df_output[transaction_tuple[0]][0:counter]=zeros_list
            
        
        if action == "sell":
            
            zeros_list=[0 for i in range(len(df_output) - counter)]
            df_output[transaction_tuple[0]][counter:len(df_output)] = zeros_list
            
        return df_output
    
    #this function is meant for transaction data but for portfolio change (return / cumulative return) not value
    def stock_change_port_return(self, df, transaction_tuple):
    
        counter = 0
        action = transaction_tuple[2]
        action = action.lower()
        
        for i in df.index:
            
            if i == transaction_tuple[1]:
                break
            
            else:
                counter += 1
                
        df_output = df.copy()
        replace_value = df_output[transaction_tuple[0]][counter]
                
        if action == "buy":
            
            replace_list = [replace_value for i in range(counter)]
            df_output[transaction_tuple[0]][0:counter] = replace_list
            
        if action == "sell":
            
            replace_list = [replace_value for i in range(len(df_output) - counter)]
            df_output[transaction_tuple[0]][counter:len(df_output)] = replace_list
            
        return df_output