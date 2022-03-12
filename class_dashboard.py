import statistics
import pandas as pd
import datetime as dt
import yfinance as yf
import streamlit as st
import plotly.express as px

class DashBoard:

    def __init__(self, market_tickers, benchmark_tickers, portfolio_value, portfolio_return, num_shares):
        
        self.market_tickers = market_tickers
        self.benchmark_tickers = benchmark_tickers
        self.portfolio_value = portfolio_value
        self.portfolio_return = portfolio_return
        self.num_shares = num_shares
        

    def get_data(self):   
        
        end_date = dt.date.today()
        start_date = dt.date(end_date.year, 1, 1)
        
        self.market_prices = yf.download(self.market_tickers, start_date, end_date)['Close']
        self.benchmark_prices = yf.download(self.benchmark_tickers, start_date, end_date)['Close']

    def portfolio_df(self):
        
        for i in range(len(self.num_shares)):
            self.portfolio_value[self.portfolio_value.columns[i]] = self.portfolio_value[self.portfolio_value.columns[i]] * float(self.num_shares[i])
    
        self.portfolio_value["total_value"] = self.portfolio_value.sum(axis =  1)
        
        self.portfolio_return["total_return"] = self.portfolio_return.sum(axis = 1)
        self.portfolio_return = self.portfolio_return.pct_change().dropna()

    def get_portfolio_value(self):
    
        current_portfolio_value = round(self.portfolio_value[self.portfolio_value.columns[len(self.portfolio_value.columns) - 1]][len(self.portfolio_value) - 1],2)
        previous_portfolio_value = round(self.portfolio_value[self.portfolio_value.columns[len(self.portfolio_value.columns) - 1]][len(self.portfolio_value) - 2],2)
       
        if current_portfolio_value < previous_portfolio_value:
            current_portfolio_value_color = "red"
        else:
            current_portfolio_value_color = "green"
            
        current_portfolio_value = "{:,}".format(current_portfolio_value)
        st.markdown("<h3 style='text-align: center; color: {};'>Portfolio Value: ${}</h3>".format(current_portfolio_value_color, current_portfolio_value), unsafe_allow_html=True)

    def daily_port_return(self):
    
        last_portfolio_return = round(self.portfolio_return[self.portfolio_return.columns[len(self.portfolio_return.columns) - 1]][len(self.portfolio_return) - 1] * 100,2)
       
        if last_portfolio_return > 0:
            current_portfolio_pct_color = "green"
        else:
            current_portfolio_pct_color = "red"
        st.markdown("<h3 style='text-align: center; color: {};'>Daily Portfolio Return: {}%</h3>".format(current_portfolio_pct_color, last_portfolio_return), unsafe_allow_html=True)

    def ytd_port(self):
    
        ytd_return = round(self.portfolio_return[self.portfolio_return.columns[len(self.portfolio_return.columns) - 1]].cumsum()[len(self.portfolio_return) - 1] * 100,2)
        
        if ytd_return > 0:
            current_portfolio_pct_color = "green"
        else:
            current_portfolio_pct_color = "red"
       
        st.markdown("<h3 style='text-align: center; color: {};'>Year to Date Return: {}%</h3>".format(current_portfolio_pct_color, ytd_return), unsafe_allow_html=True)
   
    def get_spx_daily_return(self):
    
        spx_return = round(self.benchmark_prices["^GSPC"].pct_change().dropna()[len(self.benchmark_prices) - 3] * 100,2)
       
        if spx_return > 0:
            color = "green"
        if spx_return < 0:
            color = "red"
        if spx_return == 0:
            color = "white"
            spx_return = "UNCH"

        st.markdown("<h3 style='text-align: center; color: {};'>S&P Daily Return: {}%</h3>".format(color, spx_return), unsafe_allow_html=True)
   
    def spx_ytd_return(self):
    
        spx_return_ytd = round(self.benchmark_prices["^GSPC"].pct_change().dropna().cumsum()[len(self.benchmark_prices) - 2] * 100,2)
       
        if spx_return_ytd < 0:
            color = "red"
        if spx_return_ytd > 0:
            color = "green"
       
        st.markdown("<h3 style='text-align: center; color: {};'>S&P YTD Return: {}%</h3>".format(color, spx_return_ytd), unsafe_allow_html=True)

    def get_benchmark_daily_return(self, fund_benchmark):
    
        benchmark_return = round(self.benchmark_prices[fund_benchmark].pct_change().dropna()[len(self.benchmark_prices) - 3] * 100,2)
       
        if benchmark_return > 0:
            color = "green"
        if benchmark_return < 0:
            color = "red"
        if benchmark_return == 0:
            color = "white"
            spx_return = "UNCH"
       
        st.markdown("<h3 style='text-align: center; color: {};'>{} Daily Return: {}%</h3>".format(color, fund_benchmark, benchmark_return), unsafe_allow_html=True)
   
    def benchmark_ytd_return(self, fund_benchmark):
        
        benchmark_return = round(self.benchmark_prices[fund_benchmark].pct_change().dropna().cumsum()[len(self.benchmark_prices) - 2] * 100,2)
       
        if benchmark_return < 0:
            color = "red"
        if benchmark_return > 0:
            color = "green"
       
        st.markdown("<h3 style='text-align: center; color: {};'>XLE YTD Return: {}%</h3>".format(color, benchmark_return), unsafe_allow_html=True)

    def benchmark_relative_per(self, fund_benchmark):

        benchmark_return = round(self.benchmark_prices[fund_benchmark].pct_change().dropna().cumsum()[len(self.benchmark_prices) - 2] * 100,2)
        ytd_return = round(self.portfolio_return[self.portfolio_return.columns[len(self.portfolio_return.columns) - 1]].cumsum()[len(self.portfolio_return) - 1] * 100,2)
       
        relative_performance = round(ytd_return - benchmark_return, 2)
       
        if relative_performance > 0:
            color = "green"
        if relative_performance < 0:
            color = "red"
       
        st.markdown("<h3 style='text-align: center; color: {};'>Benchmark Rel. Perf. (YTD): {}%</h3>".format(color, relative_performance), unsafe_allow_html=True)
   
    def spx_relative_per(self):

        benchmark_return = round(self.benchmark_prices["^GSPC"].pct_change().dropna().cumsum()[len(self.benchmark_prices) - 2] * 100,2)
        ytd_return = round(self.portfolio_return[self.portfolio_return.columns[len(self.portfolio_return.columns) - 1]].cumsum()[len(self.portfolio_return) - 1] * 100,2)
       
        relative_performance = round(ytd_return - benchmark_return, 2)
       
        if relative_performance > 0:
            color = "green"
        if relative_performance < 0:
            color = "red"
       
        st.markdown("<h3 style='text-align: center; color: {};'>S&P Rel. Perf. (YTD): {}%</h3>".format(color, relative_performance), unsafe_allow_html=True)

    def spx_tracking_error(self):

        market_returns = self.benchmark_prices["^GSPC"].pct_change().dropna()
        portfolio_returns = self.portfolio_return[self.portfolio_return.columns[len(self.portfolio_return.columns) - 1]]
        diff = (portfolio_returns - market_returns).dropna()
       
        tracking_error = round(statistics.stdev(diff),2)
        st.markdown("<h3 style='text-align: center; color: grey;'>S&P Tracking Err. (YTD): {}</h3>".format(tracking_error), unsafe_allow_html=True)
   
    def benchmark_tracking_error(self, fund_benchmark):
    
        market_returns = self.benchmark_prices[fund_benchmark].pct_change().dropna()
        portfolio_returns = self.portfolio_return[self.portfolio_return.columns[len(self.portfolio_return.columns) - 1]]
        diff = (portfolio_returns - market_returns).dropna()

        tracking_error = round(statistics.stdev(diff),2)
        st.markdown("<h3 style='text-align: center; color: grey;'>Benchmark Tracking Err. (YTD): {}</h3>".format(tracking_error), unsafe_allow_html=True)

    def daily_return_or_sharpe(self):
    
        rfr = self.benchmark_prices["^TNX"].dropna()
        rfr = round(rfr[len(rfr) - 1], 2)
        portfolio_returns = self.portfolio_return[self.portfolio_return.columns[len(self.portfolio_return.columns) - 1]]
        daily_average = round(portfolio_returns.mean() * 100, 2)
       
        if daily_average < rfr:
           
            if daily_average > 0:
                color = "green"
            else:
                color = "red"
           
            st.markdown("<h3 style='text-align: center; color: {};'>Daily Avg. Ret.: {}%</h3>".format(color, daily_average), unsafe_allow_html=True)
           
        else:
           
            sharpe = (daily_average - rfr) / statistics.std(portfolio_returns)
            st.markdown("<h3 style='text-align: center; color: {};'>Sharpe: {}%</h3>".format(color, sharpe), unsafe_allow_html=True)
       
    def sp_correlation(self):

        portfolio_return_val = self.portfolio_return[self.portfolio_return.columns[len(self.portfolio_return.columns) - 1]]
        market_return = self.benchmark_prices["^GSPC"].pct_change().dropna()
       
        df = pd.DataFrame({"portfolio": portfolio_return_val, "market": market_return}).dropna()
        corr = round(df.corr()[df.columns[1]][0], 2)
        st.markdown("<h3 style='text-align: center; color: grey;'>S&P Correlation: {}</h3>".format(corr), unsafe_allow_html=True)
   
    def benchmark_correlation(self, fund_benchmark):
    
        self.portfolio_return = self.portfolio_return[self.portfolio_return.columns[len(self.portfolio_return.columns) - 1]]
        market_return = self.benchmark_prices[fund_benchmark].pct_change().dropna()
       
        df = pd.DataFrame({"portfolio": self.portfolio_return, "market": market_return}).dropna()
        corr = round(df.corr()[df.columns[1]][0], 2)
        st.markdown("<h3 style='text-align: center; color: grey;'>Benchmark Correlation: {}</h3>".format(corr), unsafe_allow_html=True)
        
    def make_pie_chart(self):
    
        portfolio_weighting = self.portfolio_value.iloc[len(self.portfolio_value) - 1]
        portfolio_weighting = portfolio_weighting / portfolio_weighting[len(portfolio_weighting) - 1]
        portfolio_weighting = portfolio_weighting[:-1].to_frame()
        portfolio_weighting = portfolio_weighting.reset_index()
        portfolio_weighting.columns = ["tickers", "weights"]
       
        fig = px.pie(portfolio_weighting, values = "weights", names = "tickers", title = 'Portfolio Weighting')
        st.plotly_chart(fig)
        
    def portfolio_cum_graph(self, fund_benchmark):
    
        df = self.benchmark_prices[[fund_benchmark, "^GSPC"]].pct_change()
        df["return"] = self.portfolio_return
        df = df.dropna().cumsum()
        df = df.reset_index()
       
        df.columns = ["date", "S&P", "Benchmark", "Cumulative Return"]
        df["S&P"] = df["S&P"] * 100
        df["Benchmark"] = df["Benchmark"] * 100
        df["Cumulative Return"] = df["Cumulative Return"] * 100
        
        fig = px.line(df, x="date", y= df.columns[1:], title='Portfolio Return', width = 1000)
        st.plotly_chart(fig)
        
    def portfolio_value_graph(self):
    
        portfolio_value_df = self.portfolio_value[self.portfolio_value.columns[len(self.portfolio_value.columns) - 1]].to_frame().reset_index()
        portfolio_value_df.columns = ["date", "portfolio value"]
        fig = px.line(portfolio_value_df, x="date", y="portfolio value", title='Portfolio Value', width = 1000)
        st.plotly_chart(fig)
   