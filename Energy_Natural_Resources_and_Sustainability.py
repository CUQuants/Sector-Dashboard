import math
import time
import statistics
import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
import streamlit as st
import plotly.express as px

from PIL import Image
from class_data_manager import *

st.set_page_config(layout = "wide")

def get_data(market_tickers, benchmark_tickers):   
    
    end_date = dt.date.today()
    start_date = dt.date(end_date.year, 1, 1)
    
    market_prices = yf.download(market_tickers, start_date, end_date)['Close']
    benchmark_prices = yf.download(benchmark_tickers, start_date, end_date)['Close']
   
    return market_prices, benchmark_prices

def portfolio_df(portfolio_value, portfolio_return, num_shares):
    
    for i in range(len(num_shares)):
        portfolio_value[portfolio_value.columns[i]] = portfolio_value[portfolio_value.columns[i]] * float(num_shares[i])

    portfolio_value["total_value"] = portfolio_value.sum(axis =  1)
    
    portfolio_return["total_return"] = portfolio_return.sum(axis = 1)
    portfolio_return = portfolio_return.pct_change().dropna()
   
    return portfolio_value, portfolio_return

def market_df(market_prices):
   
    market_return = market_prices.pct_change().dropna()
   
    return market_return

def get_portfolio_value(portfolio_value):

    current_portfolio_value = round(portfolio_value[portfolio_value.columns[len(portfolio_value.columns) - 1]][len(portfolio_value) - 1],2)
    previous_portfolio_value = round(portfolio_value[portfolio_value.columns[len(portfolio_value.columns) - 1]][len(portfolio_value) - 2],2)
   
    if current_portfolio_value < previous_portfolio_value:
        current_portfolio_value_color = "red"
    else:
        current_portfolio_value_color = "green"
        
    current_portfolio_value = "{:,}".format(current_portfolio_value)
    st.markdown("<h3 style='text-align: center; color: {};'>Portfolio Value: ${}</h3>".format(current_portfolio_value_color, current_portfolio_value), unsafe_allow_html=True)

def daily_port_return(portfolio_return):

    last_portfolio_return = round(portfolio_return[portfolio_return.columns[len(portfolio_return.columns) - 1]][len(portfolio_return) - 1] * 100,2)
   
    if last_portfolio_return > 0:
        current_portfolio_pct_color = "green"
    else:
        current_portfolio_pct_color = "red"
    st.markdown("<h3 style='text-align: center; color: {};'>Daily Portfolio Return: {}%</h3>".format(current_portfolio_pct_color, last_portfolio_return), unsafe_allow_html=True)

def ytd_port(portfolio_return):

    ytd_return = round(portfolio_return[portfolio_return.columns[len(portfolio_return.columns) - 1]].cumsum()[len(portfolio_return) - 1] * 100,2)
   
    if ytd_return > 0:
        current_portfolio_pct_color = "green"
    else:
        current_portfolio_pct_color = "red"
   
    st.markdown("<h3 style='text-align: center; color: {};'>Year to Date Return: {}%</h3>".format(current_portfolio_pct_color, ytd_return), unsafe_allow_html=True)
   
def get_spx_daily_return(benchmark_prices):
   
    spx_return = round(benchmark_prices["^GSPC"].pct_change().dropna()[len(benchmark_prices) - 3] * 100,2)
   
    if spx_return > 0:
        color = "green"
    if spx_return < 0:
        color = "red"
    if spx_return == 0:
        color = "white"
        spx_return = "UNCH"
   
    st.markdown("<h3 style='text-align: center; color: {};'>S&P Daily Return: {}%</h3>".format(color, spx_return), unsafe_allow_html=True)
   
def spx_ytd_return(benchmark_prices):

    spx_return_ytd = round(benchmark_prices["^GSPC"].pct_change().dropna().cumsum()[len(benchmark_prices) - 2] * 100,2)
   
    if spx_return_ytd < 0:
        color = "red"
    if spx_return_ytd > 0:
        color = "green"
   
    st.markdown("<h3 style='text-align: center; color: {};'>S&P YTD Return: {}%</h3>".format(color, spx_return_ytd), unsafe_allow_html=True)

def get_benchmark_daily_return(benchmark_prices, fund_benchmark):
   
    benchmark_return = round(benchmark_prices[fund_benchmark].pct_change().dropna()[len(benchmark_prices) - 3] * 100,2)
   
    if benchmark_return > 0:
        color = "green"
    if benchmark_return < 0:
        color = "red"
    if benchmark_return == 0:
        color = "white"
        spx_return = "UNCH"
   
    st.markdown("<h3 style='text-align: center; color: {};'>{} Daily Return: {}%</h3>".format(color, fund_benchmark, benchmark_return), unsafe_allow_html=True)
   
def benchmark_ytd_return(benchmark_prices, fund_benchmark):

    benchmark_return = round(benchmark_prices[fund_benchmark].pct_change().dropna().cumsum()[len(benchmark_prices) - 2] * 100,2)
   
    if benchmark_return < 0:
        color = "red"
    if benchmark_return > 0:
        color = "green"
   
    st.markdown("<h3 style='text-align: center; color: {};'>XLE YTD Return: {}%</h3>".format(color, benchmark_return), unsafe_allow_html=True)

def benchmark_relative_per(benchmark_prices, portfolio_return, fund_benchmark):
   
    benchmark_return = round(benchmark_prices[fund_benchmark].pct_change().dropna().cumsum()[len(benchmark_prices) - 2] * 100,2)
    ytd_return = round(portfolio_return[portfolio_return.columns[len(portfolio_return.columns) - 1]].cumsum()[len(portfolio_return) - 1] * 100,2)
   
    relative_performance = round(ytd_return - benchmark_return, 2)
   
    if relative_performance > 0:
        color = "green"
    if relative_performance < 0:
        color = "red"
   
    st.markdown("<h3 style='text-align: center; color: {};'>Benchmark Rel. Perf. (YTD): {}%</h3>".format(color, relative_performance), unsafe_allow_html=True)
   
def spx_relative_per(benchmark_prices, portfolio_return):
   
    benchmark_return = round(benchmark_prices["^GSPC"].pct_change().dropna().cumsum()[len(benchmark_prices) - 2] * 100,2)
    ytd_return = round(portfolio_return[portfolio_return.columns[len(portfolio_return.columns) - 1]].cumsum()[len(portfolio_return) - 1] * 100,2)
   
    relative_performance = round(ytd_return - benchmark_return, 2)
   
    if relative_performance > 0:
        color = "green"
    if relative_performance < 0:
        color = "red"
   
    st.markdown("<h3 style='text-align: center; color: {};'>S&P Rel. Perf. (YTD): {}%</h3>".format(color, relative_performance), unsafe_allow_html=True)

def spx_tracking_error(benchmark_prices, portfolio_return):

    market_returns = benchmark_prices["^GSPC"].pct_change().dropna()
    portfolio_returns = portfolio_return[portfolio_return.columns[len(portfolio_return.columns) - 1]]
    diff = (portfolio_returns - market_returns).dropna()
   
    tracking_error = round(statistics.stdev(diff),2)
    st.markdown("<h3 style='text-align: center; color: grey;'>S&P Tracking Err. (YTD): {}</h3>".format(tracking_error), unsafe_allow_html=True)
   
def benchmark_tracking_error(benchmark_prices, portfolio_return, fund_benchmark):

    market_returns = benchmark_prices[fund_benchmark].pct_change().dropna()
    portfolio_returns = portfolio_return[portfolio_return.columns[len(portfolio_return.columns) - 1]]
    diff = (portfolio_returns - market_returns).dropna()
   
    tracking_error = round(statistics.stdev(diff),2)
    st.markdown("<h3 style='text-align: center; color: grey;'>Benchmark Tracking Err. (YTD): {}</h3>".format(tracking_error), unsafe_allow_html=True)

def daily_return_or_sharpe(benchmark_prices, portfolio_return):

    rfr = benchmark_prices["^TNX"].dropna()
    rfr = round(rfr[len(rfr) - 1], 2)
    portfolio_returns = portfolio_return[portfolio_return.columns[len(portfolio_return.columns) - 1]]
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
       
def sp_correlation(benchmark_prices, portfolio_return):

    daily_return_or_sharpe(benchmark_prices, portfolio_return)
   
    portfolio_return = portfolio_return[portfolio_return.columns[len(portfolio_return.columns) - 1]]
    market_return = benchmark_prices["^GSPC"].pct_change().dropna()
   
    df = pd.DataFrame({"portfolio": portfolio_return, "market": market_return}).dropna()
    corr = round(df.corr()[df.columns[1]][0], 2)
    st.markdown("<h3 style='text-align: center; color: grey;'>S&P Correlation: {}</h3>".format(corr), unsafe_allow_html=True)
   
def benchmark_correlation(benchmark_prices, portfolio_return, fund_benchmark):
   
    portfolio_return = portfolio_return[portfolio_return.columns[len(portfolio_return.columns) - 1]]
    market_return = benchmark_prices[fund_benchmark].pct_change().dropna()
   
    df = pd.DataFrame({"portfolio": portfolio_return, "market": market_return}).dropna()
    corr = round(df.corr()[df.columns[1]][0], 2)
    st.markdown("<h3 style='text-align: center; color: grey;'>Benchmark Correlation: {}</h3>".format(corr), unsafe_allow_html=True)
   
def get_brent(market_prices):
   
    current_price = round(market_prices["BZ=F"][len(market_prices) - 1],2)
   
    if current_price > market_prices["BZ=F"][len(market_prices) - 2]:
        color = "green"
    else:
        color = "red"
       

    st.markdown("<h3 style='text-align: center; color: {};'>Brent Price: ${}</h3>".format(color, current_price), unsafe_allow_html=True)

def get_crude(market_prices):
   
    current_price = round(market_prices["CL=F"][len(market_prices) - 1],2)
   
    if current_price > market_prices["CL=F"][len(market_prices) - 2]:
        color = "green"
    else:
        color = "red"
       
    st.markdown("<h3 style='text-align: center; color: {};'>Crude Price: ${}</h3>".format(color, current_price), unsafe_allow_html=True)
    
def get_nat_gas(market_prices):
    
    current_price = round(market_prices["NG=F"][len(market_prices) - 1], 2)
    
    if current_price > market_prices["NG=F"][len(market_prices) - 2]:
        color = "green"
    else:
        color = "red"
        
    st.markdown("<h3 style='text-align: center; color: {};'>Natural Gas Price: ${}</h3>".format(color, current_price), unsafe_allow_html=True)

def make_pie_chart(portfolio_value):
   
    portfolio_weighting = portfolio_value.iloc[len(portfolio_value) - 1]
    portfolio_weighting = portfolio_weighting / portfolio_weighting[len(portfolio_weighting) - 1]
    portfolio_weighting = portfolio_weighting[:-1].to_frame()
    portfolio_weighting = portfolio_weighting.reset_index()
    portfolio_weighting.columns = ["tickers", "weights"]
   
    fig = px.pie(portfolio_weighting, values = "weights", names = "tickers", title = 'Portfolio Weighting')
    st.plotly_chart(fig)
   
def portfolio_cum_graph(portfolio_return, market_prices, fund_benchmark):

    df = market_prices["^GSPC"].pct_change().to_frame()
   
    df["benchmark"] = market_prices[fund_benchmark].pct_change()
    df["ret"] = portfolio_return[portfolio_return.columns[len(portfolio_return.columns) - 1]]
    df = df.cumsum().dropna().reset_index()
   
    df.columns = ["date", "S&P", "Benchmark", "Cumulative Return"]
    df["S&P"] = df["S&P"] * 100
    df["Benchmark"] = df["Benchmark"] * 100
    df["Cumulative Return"] = df["Cumulative Return"] * 100
    
    fig = px.line(df, x="date", y= df.columns[1:], title='Portfolio Return', width = 1000)
    st.plotly_chart(fig)
   
def portfolio_value_graph(portfolio_value):

    portfolio_value_df = portfolio_value[portfolio_value.columns[len(portfolio_value.columns) - 1]].to_frame().reset_index()
    portfolio_value_df.columns = ["date", "portfolio value"]
    fig = px.line(portfolio_value_df, x="date", y="portfolio value", title='Portfolio Value', width = 1000)
    st.plotly_chart(fig)

title_col1, title_col2 = st.columns([3,1])

with title_col1:
    st.title("Leeds Investment Trading Group Fund: Energy, Natural Resources, and Sustainability")

with title_col2:
    st.image(Image.open("cuquants_logo.png"))

while True:
    
    market_tickers = ["CL=F", "NG=F", "BZ=F"] 
    benchmark_tickers = ["^GSPC", "XLE", "^TNX"]
    fund_benchmark = "XLE"
    
    data_manager = dataManager("ENERGY")

    df_return = data_manager.df_return
    df_value = data_manager.df_value
    share_num = data_manager.transactions["quantity"].to_list()
    
    market_prices, benchmark_prices = get_data(market_tickers, benchmark_tickers)
    portfolio_value, portfolio_return = portfolio_df(df_value, df_return, share_num)
    top_row1, top_row2, top_row3 = st.columns(3)
   
    with top_row1:
   
        st.markdown("<h2 style='text-align: center; color: grey;'>Portfolio Statistics</h2>", unsafe_allow_html=True)
        get_portfolio_value(portfolio_value)
        daily_port_return(portfolio_return)
        ytd_port(portfolio_return)
       
    with top_row2:
       
        st.markdown("<h2 style='text-align: center; color: grey;'>Market Statistics</h2>", unsafe_allow_html=True)
        get_spx_daily_return(benchmark_prices)
        spx_ytd_return(benchmark_prices)
        get_benchmark_daily_return(benchmark_prices, fund_benchmark)
        benchmark_ytd_return(benchmark_prices, fund_benchmark)
     
    with top_row3:
       
        st.markdown("<h2 style='text-align: center; color: grey;'>Relative Statistics</h2>", unsafe_allow_html=True)
        spx_relative_per(benchmark_prices, portfolio_return)
        benchmark_relative_per(benchmark_prices, portfolio_return, fund_benchmark)
        spx_tracking_error(benchmark_prices, portfolio_return)
        benchmark_tracking_error(benchmark_prices, portfolio_return, fund_benchmark)
   
    second_row1, second_row2, second_row3 = st.columns(3)
   
    with second_row1:
       
        st.markdown("<h2 style='text-align: center; color: grey;'></h2>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'></h2>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'></h2>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Market Info</h2>", unsafe_allow_html=True)
        sp_correlation(benchmark_prices, portfolio_return)
        benchmark_correlation(benchmark_prices, portfolio_return, fund_benchmark)
       
    with second_row2:
       
        st.markdown("<h2 style='text-align: center; color: grey;'></h2>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'></h2>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'></h2>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Sector Securities</h2>", unsafe_allow_html=True)
        get_brent(market_prices)
        get_crude(market_prices)
        get_nat_gas(market_prices)
   
    with second_row3:
       
        make_pie_chart(portfolio_value)
       
    third_row1, third_row2 = st.columns(2)
   
    with third_row1:
        portfolio_cum_graph(portfolio_return, benchmark_prices, fund_benchmark)
       
    with third_row2:
        portfolio_value_graph(portfolio_value)
   
    next_update = dt.datetime.today() + dt.timedelta(seconds = 60 * 60 * 4)
    next_update_time = next_update.strftime("%a %D %I:%M %p")
    st.write("next update is scheduled for {}".format(next_update_time))

    st.write("Information does not constitute as investment advice")
    st.write("Errors may occur due to rounding and outdated information provided, updates do not occur until trading day ends")
    st.write("Dashboard created and maintained by CU Quants, not associated with Leeds Investment Trading Group (LITG) Fund")
    st.write("Investment Decision handled by Leeds Investment Trading Group (LITG) and not CU Quants")
    
    st.write("Using prices from this date:", df_value.index[len(df_value) - 1])
   
    time.sleep(60 * 60 * 4)