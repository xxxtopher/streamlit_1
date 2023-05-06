import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
import requests
from bs4 import BeautifulSoup
from newsapi import NewsApiClient

# Set up NewsAPI
newsapi = NewsApiClient(api_key='7b36370fdca94d0eba309efc7819b48c')

# Define a function to get news headlines
def get_news_headlines(query):
    news_headlines = []
    news_articles = newsapi.get_everything(q=query, sort_by='relevancy', language='en', page_size=5)['articles']
    for article in news_articles:
        news_headlines.append(article['title'])
    return news_headlines

# Define a function to get stock news from Yahoo Finance
def get_stock_news(ticker):
    stock_news = []
    url = f"https://finance.yahoo.com/quote/{ticker}/news?p={ticker}"
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    for item in soup.find_all('div', {'class': 'Mb(5px)'}):
        stock_news.append(item.a.text)
    return stock_news

# Define the Streamlit app
st.title("Stock Price Dashboard")
st.write("Enter a stock symbol to see its current price and recent news.")

# Get user input for stock symbol
ticker = st.text_input("Enter stock symbol (e.g. AAPL):")

# Get stock data
stock_data = yf.Ticker(ticker).history(period='1y')
latest_price = stock_data['Close'][-1]

# Display stock chart
fig = go.Figure(data=[go.Candlestick(x=stock_data.index,
                open=stock_data['Open'],
                high=stock_data['High'],
                low=stock_data['Low'],
                close=stock_data['Close'])])
st.plotly_chart(fig)

# Get news headlines for the stock
news_headlines = get_news_headlines(ticker)
stock_news = get_stock_news(ticker)

# Display news headlines
st.write(f"Latest price for {ticker}: {latest_price}")
st.write("News Headlines:")
for headline in news_headlines:
    st.write(headline)

st.write("Stock News:")
for news in stock_news:
    st.write(news)
