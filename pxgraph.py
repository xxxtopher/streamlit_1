import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime, timedelta, date
import streamlit as st
from bs4 import BeautifulSoup
import requests

# Function to fetch ticker options from Alpha Vantage API based on user input
def get_ticker_options(query):
    api_key = '9TOHVS9OP9X69QCH'
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'SYMBOL_SEARCH',
        'keywords': query,
        'apikey': api_key
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if 'bestMatches' in data:
        return [match['1. symbol'] for match in data['bestMatches']]
    else:
        return []

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
                      yaxis_title="Price",
                      height=600)

    # Remove non-trading days
    trading_days = pd.date_range(start=stock_data['Date'].min(), end=stock_data['Date'].max(), freq='D')
    fig.update_xaxes(type='category', categoryorder='array', categoryarray=[str(day.date()) for day in trading_days])

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
stock_ticker_input = st.sidebar.text_input("Enter stock ticker (e.g. AAPL):")

# Fetch ticker options from Alpha Vantage API based on user input
ticker_options = get_ticker_options(stock_ticker_input)

# Use datalist HTML element for the dropdown list
st.sidebar.markdown("<label for='ticker_input'>Choose a ticker:</label>", unsafe_allow_html=True)
st.sidebar.markdown(f"<input list='tickers' id='ticker_input' name='ticker_input' value='{stock_ticker_input}'>", unsafe_allow_html=True)
st.sidebar.markdown("<datalist id='tickers'>", unsafe_allow_html=True)
for ticker in ticker_options:
    st.sidebar.markdown(f"<option value='{ticker}'>", unsafe_allow_html=True)
st.sidebar.markdown("</datalist>", unsafe_allow_html=True)

# Get the current date
current_date = datetime.now()

# Set the default end date to the current date
end_date = st.sidebar.date_input("Enter end date:", current_date)

# Set the default start date to one year before the end date
default_start_date = current_date - timedelta(days=365)
start_date = st.sidebar.date_input("Enter start date:", default_start_date)

if stock_ticker_input and start_date and end_date:

    # Download stock price data
    stock_data = download_stock_data(stock_ticker_input, start_date, end_date)

    # Create Candlestick Chart
    st.plotly_chart(create_candlestick_chart(stock_data))

    # Search stock news
    articles = search_stock_news(stock_ticker_input)

    # Display stock news
    st.subheader(f"{stock_ticker_input} News")
    if not articles:
        st.write("No news found")
    else:
        for article in articles:
            st.write(article["title"])
            st.write(article["description"])
            st.write(article["url"])
            st.write("---")

