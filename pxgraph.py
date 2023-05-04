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


def display_stock_news(stock_ticker):
    query = stock_ticker + " news"
    url = f"https://www.google.com/search?q={query}&tbm=nws&ei=6X9aYZKjJYS4rQG58bCwDw&ved=0ahUKEwj2rJikxMjzAhXOnpUCHTf7Dwo4ChDy0wMIqgE&rlz=1C1GCEA_enUS832US832&oq=Apple+news&gs_l=psy-ab.3..35i39l2j0l2j0i131i67j0i67j0i131i67j0i67l2j0i131i67j0i131i20i263j0i20i263j0i131i20i263j0i20i263j0i131i67.10236.11432.0.11871.8.8.0.0.0.0.224.904.2-4.4.0....0...1c.1.64.psy-ab..4.4.902....0.CPymF5TDWfI"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    search_results = soup.find_all('div', {'class': 'dbsr'})

    for i, result in enumerate(search_results):
        if i == 5:
            break
        title = result.find('div', {'class': 'JheGif nDgy9d'}).get_text()
        link = result.a['href']
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
    st.plotly_chart(create_candlestick_chart(stock_data))

    # Display Stock News
    st.subheader("Stock News in the Past Month")
    display_stock_news(stock_ticker)
