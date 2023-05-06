import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime, timedelta
import streamlit as st
from bs4 import BeautifulSoup
import requests

# Download stock data
def download_stock_data(stock_ticker, start_date, end_date):
    stock_data = yf.download(stock_ticker, start=start_date, end=end_date)
    stock_data.reset_index(inplace=True)
    stock_data["Date"] = stock_data["Date"].dt.strftime('%Y-%m-%d')
    return stock_data


def create_candlestick_chart(stock_data):
    fig = go.Figure(data=[go.Candlestick(x=stock_data['Date'],
                                         open=stock_data['Open'],
                                         high=stock_data['High'],
                                         low=stock_data['Low'],
                                         close=stock_data['Close'])])
    fig.update_layout(title=f"{stock_ticker} Candlestick Chart",
                      xaxis_title="Date",
                      yaxis_title="Price")
    return fig

def search_stock_news(stock_ticker):
    api_key = '7b36370fdca94d0eba309efc7819b48c'
    query = stock_ticker
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}&sortBy=publishedAt&pageSize=10"
    response = requests.get(url)
    articles = response.json()["articles"]
    return articles


# Main Streamlit app
st.set_page_config(page_title="Hong Kong Stock Analysis Dashboard", page_icon=":chart_with_upwards_trend:")
st.title("Stock Analysis Dashboard")

# Get user input for stock ticker and date range
stock_ticker = st.sidebar.text_input("Enter stock ticker (e.g. 0001.HK):")
start_date = st.sidebar.date_input("Enter start date:")
end_date = st.sidebar.date_input("Enter end date:")

if stock_ticker and start_date and end_date:

    # Download stock price data
    stock_data = download_stock_data(stock_ticker, start_date, end_date)

    # Create Candlestick Chart
    st.plotly_chart(create_candlestick_chart(stock_data))

    # Search stock news
    articles = search_stock_news(stock_ticker)

    # Display stock news
    st.subheader(f"{stock_ticker} News")
    if not articles:
        st.write("No news found")
    else:
        for article in articles:
            st.write(article["title"])
            st.write(article["description"])
            st.write(article["url"])
            st.write("---")

