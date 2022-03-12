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
from class_dashboard import *
from class_data_manager import *

def get_micro(market_prices):
    
    last_price = round(market_prices["10Y=F"][len(market_prices) - 1],2)
    st.markdown("<h3 style='text-align: center; color: grey;'>Micro 10Y Future: {}%</h3>".format(last_price), unsafe_allow_html=True)
    
def get_emini(market_prices):

    current_price = round(market_prices["ES=F"][len(market_prices) - 1],2)
   
    if current_price > market_prices["ES=F"][len(market_prices) - 2]:
        color = "green"
    else:
        color = "red"

    st.markdown("<h3 style='text-align: center; color: {};'>S&P E-Mini: ${}</h3>".format(color, current_price), unsafe_allow_html=True)
    
def get_treasury(market_prices):
    
    current_price = round(market_prices["^TNX"][len(market_prices) - 1],2)
   
    if current_price > market_prices["^TNX"][len(market_prices) - 2]:
        color = "green"
    else:
        color = "red"

    st.markdown("<h3 style='text-align: center; color: {};'>S&10Y {}%</h3>".format(color, current_price), unsafe_allow_html=True)
    
st.set_page_config(layout = "wide")

title_col1, title_col2 = st.columns([3,1])

with title_col1:
    st.title("Leeds Investment Trading Group Fund: Consumer")

with title_col2:
    st.image(Image.open("cuquants_logo.png"))

while True:
    
    market_tickers = ["10Y=F", "^TNX", "ES=F"] 
    benchmark_tickers = ["^GSPC", "XLY", "^TNX"]
    fund_benchmark = "XLY"
    
    data_manager = dataManager("CONSUMER")

    df_return = data_manager.df_return
    df_value = data_manager.df_value
    share_num = data_manager.transactions["quantity"].to_list()
    
    dashboard = DashBoard(market_tickers, benchmark_tickers, df_value, df_return, share_num)
    dashboard.get_data()
    market_prices, benchmark_prices = dashboard.market_prices, dashboard.benchmark_prices
    
    dashboard.portfolio_df()
    portfolio_value, portfolio_return = dashboard.portfolio_value, dashboard.portfolio_return
    top_row1, top_row2, top_row3 = st.columns(3)
   
    with top_row1:
   
        st.markdown("<h2 style='text-align: center; color: grey;'>Portfolio Statistics</h2>", unsafe_allow_html=True)
        dashboard.get_portfolio_value()
        dashboard.daily_port_return()
        dashboard.ytd_port()
       
    with top_row2:
       
        st.markdown("<h2 style='text-align: center; color: grey;'>Market Statistics</h2>", unsafe_allow_html=True)
        dashboard.get_spx_daily_return()
        dashboard.spx_ytd_return()
        dashboard.get_benchmark_daily_return(fund_benchmark)
        dashboard.benchmark_ytd_return(fund_benchmark)
     
    with top_row3:
       
        st.markdown("<h2 style='text-align: center; color: grey;'>Relative Statistics</h2>", unsafe_allow_html=True)
        dashboard.spx_relative_per()
        dashboard.benchmark_relative_per(fund_benchmark)
        dashboard.spx_tracking_error()
        dashboard.benchmark_tracking_error(fund_benchmark)
   
    second_row1, second_row2, second_row3 = st.columns(3)
   
    with second_row1:
       
        st.markdown("<h2 style='text-align: center; color: grey;'></h2>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'></h2>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'></h2>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Market Info</h2>", unsafe_allow_html=True)
        dashboard.daily_return_or_sharpe()
        dashboard.sp_correlation()
        dashboard.benchmark_correlation(fund_benchmark)
       
    with second_row2:
       
        st.markdown("<h2 style='text-align: center; color: grey;'></h2>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'></h2>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'></h2>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Sector Securities</h2>", unsafe_allow_html=True)
        get_micro(market_prices)
        get_emini(market_prices)
        get_treasury(market_prices)
        
    with second_row3:
       
        dashboard.make_pie_chart()
       
    third_row1, third_row2 = st.columns(2)
   
    with third_row1:
        dashboard.portfolio_cum_graph(fund_benchmark)
       
    with third_row2:
        dashboard.portfolio_value_graph()
   
    next_update = dt.datetime.today() + dt.timedelta(seconds = 60 * 60 * 4)
    next_update_time = next_update.strftime("%a %D %I:%M %p")
    st.write("next update is scheduled for {}".format(next_update_time))

    st.write("Information does not constitute as investment advice")
    st.write("Errors may occur due to rounding and outdated information provided, updates do not occur until trading day ends")
    st.write("Dashboard created and maintained by CU Quants, not associated with Leeds Investment Trading Group (LITG) Fund")
    st.write("Investment Decision handled by Leeds Investment Trading Group (LITG) and not CU Quants")
    
    st.write("Using prices from this date:", df_value.index[len(df_value) - 1])
   
    time.sleep(60 * 60 * 4)