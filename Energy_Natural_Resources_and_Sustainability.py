import math
import time
import statistics
import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
import streamlit as st
import plotly.express as px

st.set_page_config(layout = "wide")

def get_data():

    end_date = dt.date.today()
    start_date = dt.date(end_date.year, 1, 1)
   
    port_tickers = ["EOG", "OKE", "SRE"]
    market_tickers = ["CL=F", "NG=F", "BZ=F", "^GSPC", "XLE", "^TNX"]
   
    stock_prices = yf.download(port_tickers, start_date, end_date)['Close']
    market_prices = yf.download(market_tickers, start_date, end_date)['Close']
   
    return stock_prices, market_prices

def portfolio_df(stock_prices):

    number_of_shares = [66, 95, 43]
    portfolio_value = stock_prices.copy()
   
    for i in range(len(number_of_shares)):
        portfolio_value[portfolio_value.columns[i]] = portfolio_value[portfolio_value.columns[i]] * number_of_shares[i]
       
    portfolio_value["total_value"] = portfolio_value.sum(axis =  1)
    portfolio_return = portfolio_value.pct_change().dropna()
   
    return portfolio_value, portfolio_return

def market_df(market_prices):
   
    market_return = market_prices.pct_change().dropna()
   
    return market_return

def get_portfolio_value():

    current_portfolio_value = round(portfolio_value[portfolio_value.columns[len(portfolio_value.columns) - 1]][len(portfolio_value) - 1],2)
    previous_portfolio_value = round(portfolio_value[portfolio_value.columns[len(portfolio_value.columns) - 1]][len(portfolio_value) - 2],2)
   
    if current_portfolio_value < previous_portfolio_value:
        current_portfolio_value_color = "red"
    else:
        current_portfolio_value_color = "green"
   
    st.markdown("<h3 style='text-align: center; color: {};'>Portfolio Value: ${}</h3>".format(current_portfolio_value_color, current_portfolio_value), unsafe_allow_html=True)

def daily_port_return(portfolio_return):

    last_portfolio_return = round(portfolio_return[portfolio_return.columns[len(portfolio_return.columns) - 1]][len(portfolio_return) - 1] * 100,2)
   
    if last_portfolio_return > 0:
        current_portfolio_pct_color = "green"
    else:
        current_portfolio_pct_color = "red"
       
    st.markdown("<h3 style='text-align: center; color: {};'>Daily Portfolio Return: {}%</h3>".format(current_portfolio_pct_color, last_portfolio_return), unsafe_allow_html=True)

st.title("Leeds Investment Trading Group Fund: Energy, Natural Resources, and Sustainability")

def ytd_port(portfolio_return):

    ytd_return = round(portfolio_return[portfolio_return.columns[len(portfolio_return.columns) - 1]].cumsum()[len(portfolio_return) - 1] * 100,2)
   
    if ytd_return > 0:
        current_portfolio_pct_color = "green"
    else:
        current_portfolio_pct_color = "red"
   
    st.markdown("<h3 style='text-align: center; color: {};'>Year to Date Return: {}%</h3>".format(current_portfolio_pct_color, ytd_return), unsafe_allow_html=True)
   
def get_spx_daily_return(market_prices):
   
    spx_return = round(market_prices["^GSPC"].pct_change().dropna()[len(market_prices) - 3] * 100,2)
   
    if spx_return > 0:
        color = "green"
    if spx_return < 0:
        color = "red"
    if spx_return == 0:
        color = "white"
        spx_return = "UNCH"
   
    st.markdown("<h3 style='text-align: center; color: {};'>S&P Daily Return: {}%</h3>".format(color, spx_return), unsafe_allow_html=True)
   
def spx_ytd_return(market_prices):

    spx_return_ytd = round(market_prices["^GSPC"].pct_change().dropna().cumsum()[len(market_prices) - 2] * 100,2)
   
    if spx_return_ytd < 0:
        color = "red"
    if spx_return_ytd > 0:
        color = "green"
   
    st.markdown("<h3 style='text-align: center; color: {};'>S&P YTD Return: {}%</h3>".format(color, spx_return_ytd), unsafe_allow_html=True)

def get_benchmark_daily_return(market_prices):
   
    benchmark_return = round(market_prices["XLE"].pct_change().dropna()[len(market_prices) - 3] * 100,2)
   
    if benchmark_return > 0:
        color = "green"
    if benchmark_return < 0:
        color = "red"
    if benchmark_return == 0:
        color = "white"
        spx_return = "UNCH"
   
    st.markdown("<h3 style='text-align: center; color: {};'>XLE Daily Return: {}%</h3>".format(color, benchmark_return), unsafe_allow_html=True)
   
def benchmark_ytd_return(market_prices):

    benchmark_return = round(market_prices["XLE"].pct_change().dropna().cumsum()[len(market_prices) - 2] * 100,2)
   
    if benchmark_return < 0:
        color = "red"
    if benchmark_return > 0:
        color = "green"
   
    st.markdown("<h3 style='text-align: center; color: {};'>XLE YTD Return: {}%</h3>".format(color, benchmark_return), unsafe_allow_html=True)

def benchmark_relative_per(market_prices, portfolio_return):
   
    benchmark_return = round(market_prices["XLE"].pct_change().dropna().cumsum()[len(market_prices) - 2] * 100,2)
    ytd_return = round(portfolio_return[portfolio_return.columns[len(portfolio_return.columns) - 1]].cumsum()[len(portfolio_return) - 1] * 100,2)
   
    relative_performance = ytd_return - benchmark_return
   
    if relative_performance > 0:
        color = "green"
    if relative_performance < 0:
        color = "red"
   
    st.markdown("<h3 style='text-align: center; color: {};'>Benchmark Rel. Perf. (YTD): {}%</h3>".format(color, relative_performance), unsafe_allow_html=True)
   
def spx_relative_per(market_prices, portfolio_return):
   
    benchmark_return = round(market_prices["^GSPC"].pct_change().dropna().cumsum()[len(market_prices) - 2] * 100,2)
    ytd_return = round(portfolio_return[portfolio_return.columns[len(portfolio_return.columns) - 1]].cumsum()[len(portfolio_return) - 1] * 100,2)
   
    relative_performance = ytd_return - benchmark_return
   
    if relative_performance > 0:
        color = "green"
    if relative_performance < 0:
        color = "red"
   
    st.markdown("<h3 style='text-align: center; color: {};'>S&P Rel. Perf. (YTD): {}%</h3>".format(color, relative_performance), unsafe_allow_html=True)

def spx_tracking_error(market_prices, portfolio_return):

    market_returns = market_prices["^GSPC"].pct_change().dropna()
    portfolio_returns = portfolio_return[portfolio_return.columns[len(portfolio_return.columns) - 1]]
    diff = (portfolio_returns - market_returns).dropna()
   
    tracking_error = round(statistics.stdev(diff),2)
    st.markdown("<h3 style='text-align: center; color: white;'>S&P Tracking Err. (YTD): {}</h3>".format(tracking_error), unsafe_allow_html=True)
   
def benchmark_tracking_error(market_prices, portfolio_return):

    market_returns = market_prices["XLE"].pct_change().dropna()
    portfolio_returns = portfolio_return[portfolio_return.columns[len(portfolio_return.columns) - 1]]
    diff = (portfolio_returns - market_returns).dropna()
   
    tracking_error = round(statistics.stdev(diff),2)
    st.markdown("<h3 style='text-align: center; color: white;'>Benchmark Tracking Err. (YTD): {}</h3>".format(tracking_error), unsafe_allow_html=True)

def daily_return_or_sharpe(market_prices, portfolio_return):

    rfr = market_prices["^TNX"].dropna()
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
       
def sp_correlation(market_prices, portfolio_return):

    daily_return_or_sharpe(market_prices, portfolio_return)
   
    portfolio_return = portfolio_return[portfolio_return.columns[len(portfolio_return.columns) - 1]]
    market_return = market_prices["^GSPC"].pct_change().dropna()
   
    df = pd.DataFrame({"portfolio": portfolio_return, "market": market_return}).dropna()
    corr = round(df.corr()[df.columns[1]][0], 2)
    st.markdown("<h3 style='text-align: center; color: white;'>S&P Correlation: {}</h3>".format(corr), unsafe_allow_html=True)
   
def benchmark_correlation(market_prices, portfolio_return):
   
    portfolio_return = portfolio_return[portfolio_return.columns[len(portfolio_return.columns) - 1]]
    market_return = market_prices["XLE"].pct_change().dropna()
   
    df = pd.DataFrame({"portfolio": portfolio_return, "market": market_return}).dropna()
    corr = round(df.corr()[df.columns[1]][0], 2)
    st.markdown("<h3 style='text-align: center; color: white;'>Benchmark Correlation: {}</h3>".format(corr), unsafe_allow_html=True)
   
def get_brent(market_prices):
   
    current_price = round(market_prices["BZ=F"][len(market_prices) - 1],2)
   
    if current_price > market_prices["BZ=F"][len(market_prices) - 2]:
        color = "green"
    else:
        color = "red"
       
    st.markdown("<h3 style='text-align: center; color: {};'>Brent Price: {}</h3>".format(color, current_price), unsafe_allow_html=True)

def get_crude(market_prices):
   
    current_price = round(market_prices["CL=F"][len(market_prices) - 1],2)
   
    if current_price > market_prices["CL=F"][len(market_prices) - 2]:
        color = "green"
    else:
        color = "red"
       
    st.markdown("<h3 style='text-align: center; color: {};'>Crude Price: {}</h3>".format(color, current_price), unsafe_allow_html=True)
   
def make_pie_chart(portfolio_value):
   
    portfolio_weighting = portfolio_value.iloc[len(portfolio_value) - 1]
    portfolio_weighting = portfolio_weighting / portfolio_weighting[len(portfolio_weighting) - 1]
    portfolio_weighting = portfolio_weighting[:-1].to_frame()
    portfolio_weighting = portfolio_weighting.reset_index()
    portfolio_weighting.columns = ["tickers", "weights"]
   
    fig = px.pie(portfolio_weighting, values = "weights", names = "tickers", title = 'Portfolio Weighting')
    st.plotly_chart(fig)
   
def portfolio_cum_graph(portfolio_return, market_prices):

    df = market_prices["^GSPC"].pct_change().to_frame()
   
    df["benchmark"] = market_prices["XLE"].pct_change()
    df["ret"] = portfolio_return[portfolio_return.columns[len(portfolio_return.columns) - 1]]
    df = df.cumsum().dropna().reset_index()
   
    df.columns = ["date", "S&P", "Benchmark", "Cumulative Return"]
    fig = px.line(df, x="date", y= df.columns[1:] * 100, title='Portfolio Return', width = 1000)
    st.plotly_chart(fig)
   
def portfolio_value_graph(portfolio_value):

    portfolio_value_df = portfolio_value[portfolio_value.columns[len(portfolio_value.columns) - 1]].to_frame().reset_index()
    portfolio_value_df.columns = ["date", "portfolio value"]
    fig = px.line(portfolio_value_df, x="date", y="portfolio value", title='Portfolio Value', width = 1000)
    st.plotly_chart(fig)

while True:

    update_date = dt.datetime.today().strftime("%a %D %I:%M %p")
    st.header("last updated: {}".format(update_date))
    st.write("Sector Head: Joseph Fratino Jr. (MVP)")
   
    stock_prices, market_prices = get_data()
    portfolio_value, portfolio_return = portfolio_df(stock_prices)
   
    top_row1, top_row2, top_row3 = st.columns(3)
   
    with top_row1:
   
        st.markdown("<h2 style='text-align: center; color: white;'>Portfolio Statistics</h2>", unsafe_allow_html=True)
        get_portfolio_value()
        daily_port_return(portfolio_return)
        ytd_port(portfolio_return)
       
    with top_row2:
       
        st.markdown("<h2 style='text-align: center; color: white;'>Market Statistics</h2>", unsafe_allow_html=True)
        get_spx_daily_return(market_prices)
        spx_ytd_return(market_prices)
        get_benchmark_daily_return(market_prices)
        benchmark_ytd_return(market_prices)
     
    with top_row3:
       
        st.markdown("<h2 style='text-align: center; color: white;'>Relative Statistics</h2>", unsafe_allow_html=True)
        spx_relative_per(market_prices, portfolio_return)
        benchmark_relative_per(market_prices, portfolio_return)
        spx_tracking_error(market_prices, portfolio_return)
        benchmark_tracking_error(market_prices, portfolio_return)
   
    second_row1, second_row2, second_row3 = st.columns(3)
   
    with second_row1:
       
        st.markdown("<h2 style='text-align: center; color: white;'></h2>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: white;'></h2>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: white;'></h2>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: white;'>Market Info</h2>", unsafe_allow_html=True)
        sp_correlation(market_prices, portfolio_return)
        benchmark_correlation(market_prices, portfolio_return)
       
    with second_row2:
       
        st.markdown("<h2 style='text-align: center; color: white;'></h2>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: white;'></h2>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: white;'></h2>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: white;'></h2>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: white;'>Market Prices</h2>", unsafe_allow_html=True)
        get_brent(market_prices)
        get_crude(market_prices)
   
    with second_row3:
       
        make_pie_chart(portfolio_value)
       
    third_row1, third_row2 = st.columns(2)
   
    with third_row1:
        portfolio_cum_graph(portfolio_return, market_prices)
       
    with third_row2:
        portfolio_value_graph(portfolio_value)
   
    next_update = dt.datetime.today() + dt.timedelta(seconds = 60 * 60 * 4)
    next_update_time = next_update.strftime("%a %D %I:%M %p")
    st.write("next update is scheduled for {}".format(next_update_time))

    st.write("Information does not constitute as investment advice")
    st.write("Errors may occur due to rounding and outdated information provided, updates do not occur until trading day ends")
    st.write("Dashboard created and maintained by CU Quants, not associated with Leeds Investment Trading Group (LITG) Fund")
    st.write("Investment Decision handled by Leeds Investment Trading Group (LITG) and not CU Quants")
   
    time.sleep(60 * 60 * 4)
