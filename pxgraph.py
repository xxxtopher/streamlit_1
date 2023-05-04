import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime, timedelta
import streamlit as st
from bs4 import BeautifulSoup
import requests


def download_stock_data(stock_ticker, start_date, end_date):
    stock_data = yf.download(stock_ticker, start=start_date, end=end_date)
    stock_data.reset_index(inplace=True)
    stock_data["Date"] = stock_data["Date"].dt.strftime('%Y-%m-%d')
    return stock_data


def create_candlestick_chart(stock_data, stock_ticker):
    fig = go.Figure(data=[go.Candlestick(x=stock_data['Date'],
                                         open=stock_data['Open'],
                                         high=stock_data['High'],
                                         low=stock_data['Low'],
                                         close=stock_data['Close'])])
    fig.update_layout(title=f"{stock_ticker} Candlestick Chart",
                      xaxis_title="Date",
                      yaxis_title="Price")
    return fig


def display_stock_news(stock_ticker):
    query = f"{stock_ticker} stock news"
    url = f"https://www.google.com/search?q={query}&tbm=nws&tbs=qdr:m"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    news_items = soup.select(".dbsr")
    if not news_items:
        st.write("No news articles found.")
    else:
        for item in news_items:
            title = item.find("div", class_="JheGif nDgy9d").get_text()
            link = item.find("a", href=True)['href']
            st.write(f"[{title}]({link})")


# Main Streamlit app
st.title("Hong Kong Stock Analysis Dashboard")

# Get user input for stock ticker and date range
stock_ticker = st.text_input("Enter stock ticker (e.g. 0001.HK):")
start_date = st.date_input("Enter start date:")
end_date = st.date_input("Enter end date:")

if stock_ticker and start_date and end_date:

    # Download stock price data
    stock_data = download_stock_data(stock_ticker, start_date, end_date)

    # Create Candlestick Chart
    st.plotly_chart(create_candlestick_chart(stock_data, stock_ticker))

    # Display Stock News
    st.subheader(f"{stock_ticker} News")
    display_stock_news(stock_ticker)
