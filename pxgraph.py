import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime, timedelta
import streamlit as st
from bs4 import BeautifulSoup
import requests

# Set up News API
newsapi = NewsApiClient(api_key='7b36370fdca94d0eba309efc7819b48c')

# Function to download stock data
def download_stock_data(stock_ticker, start_date, end_date):
    stock_data = yf.download(stock_ticker, start=start_date, end=end_date)
    stock_data.reset_index(inplace=True)
    stock_data["Date"] = stock_data["Date"].dt.strftime('%Y-%m-%d')
    return stock_data

# Function to create candlestick chart
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

# Function to search news related to stock ticker
def search_news(stock_ticker):
    query = f"{stock_ticker} stock news"
    newsapi = NewsApiClient(api_key='7b36370fdca94d0eba309efc7819b48c')
    top_headlines = newsapi.get_top_headlines(q=query, language='en', page_size=5)
    articles = top_headlines['articles']
    if len(articles) < 5:
        remaining = 5 - len(articles)
        for j in search(query, num=remaining, lang='en', pause=2):
            article = {}
            article['title'] = j['title']
            article['url'] = j['link']
            article['description'] = j['snippet']
            article['source'] = j['source']['name']
            article['publishedAt'] = j['pubDate']
            articles.append(article)
    return articles

# Main Streamlit app
st.set_page_config(layout="wide")
st.title("Stock Analysis Dashboard")

# Get user input for stock ticker and date range
stock_ticker = st.sidebar.text_input("Enter stock ticker (e.g. 0001.HK):")
start_date = st.sidebar.date_input("Enter start date:")
end_date = st.sidebar.date_input("Enter end date:")

if stock_ticker and start_date and end_date:

    # Download stock price data
    stock_data = download_stock_data(stock_ticker, start_date, end_date)

    # Create Candlestick Chart
    st.plotly_chart(create_candlestick_chart(stock_data, stock_ticker))

    # Display news related to stock ticker
    st.subheader(f"Latest news for {stock_ticker}")
    news = search_news(stock_ticker)
    if news:
        for article in news:
            st.write(f"- [{article['title']}]({article['url']})")
    else:
        st.write("No news found.")
