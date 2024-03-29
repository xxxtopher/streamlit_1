import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta
import streamlit as st
import requests

base = "dark"
primaryColor = "black"

# Function to fetch stock data from Yahoo Finance
def download_stock_data(stock_ticker, start_date, end_date):
    stock_data = yf.download(stock_ticker, start=start_date, end=end_date)
    stock_data.reset_index(inplace=True)
    stock_data["Date"] = stock_data["Date"].dt.strftime('%Y-%m-%d')
    return stock_data

# Function to create a candlestick chart with moving average lines
def create_candlestick_chart_with_ma(stock_data, show_ma_10, show_ma_20, show_ma_50, show_ma_100, show_ma_200):
    fig = go.Figure()

    # Candlestick trace
    fig.add_trace(go.Candlestick(x=stock_data['Date'],
                                 open=stock_data['Open'],
                                 high=stock_data['High'],
                                 low=stock_data['Low'],
                                 close=stock_data['Close'], name='Candlestick'))

    # Moving average traces
    ma_colors = ["white", "red", "green", "blue", "purple"]

    if show_ma_10:
        fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Close'].rolling(window=10).mean(),
                                 mode='lines', name='MA 10', line=dict(color=ma_colors[0])))
    if show_ma_20:
        fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Close'].rolling(window=20).mean(),
                                 mode='lines', name='MA 20', line=dict(color=ma_colors[1])))
    if show_ma_50:
        fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Close'].rolling(window=50).mean(),
                                 mode='lines', name='MA 50', line=dict(color=ma_colors[2])))
    if show_ma_100:
        fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Close'].rolling(window=100).mean(),
                                 mode='lines', name='MA 100', line=dict(color=ma_colors[3])))
    if show_ma_200:
        fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Close'].rolling(window=200).mean(),
                                 mode='lines', name='MA 200', line=dict(color=ma_colors[4])))

    fig.update_layout(title=f"{selected_ticker} Candlestick Chart with Moving Averages",
                      title_font_color="white",
                      legend_title_font_color="white",
                      xaxis_title="Date",
                      yaxis_title="Price",
                      paper_bgcolor="#000000",
                      plot_bgcolor="#000000",
                      width=1200,
                      height=600)

    # Remove non-trading days
    trading_days = pd.date_range(start=stock_data['Date'].min(), end=stock_data['Date'].max(), freq='D')
    fig.update_xaxes(type='category', categoryorder='array', categoryarray=[str(day.date()) for day in trading_days])

    return fig

# Function to fetch news articles data from Finnhub API
def fetch_news_data(stock_ticker):
    finnhub_api_key = 'ciu3hapr01qkv67u3n50ciu3hapr01qkv67u3n5g'
    url = f'https://finnhub.io/api/v1/company-news'
    params = {
        'symbol': stock_ticker,
        'from': (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'),
        'to': datetime.now().strftime('%Y-%m-%d'),
        'token': finnhub_api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

# Main Streamlit app
st.set_page_config(page_title="Stock Analysis Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")
st.title("Stock Analysis Dashboard")

# Create a sidebar for input widgets
st.sidebar.title("Stock Analysis Options")

# Get user input for stock ticker and date range
selected_ticker = st.sidebar.text_input("Enter stock ticker (e.g. AAPL):")

# Get the current date
current_date = datetime.now()

# Set the default end date to the current date
end_date = st.sidebar.date_input("Enter end date:", current_date)

# Set the default start date to one year before the end date
default_start_date = current_date - timedelta(days=365)
start_date = st.sidebar.date_input("Enter start date:", default_start_date)

# Custom CSS to display tick-box buttons horizontally
horizontal_style = """
<style>
    .horizontal-checkboxes {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        margin-bottom: 20px;
    }
</style>
"""
st.markdown(horizontal_style, unsafe_allow_html=True)

# Tick-box buttons for moving average lines, displayed horizontally
st.markdown("### Moving Averages")
st.markdown('<div class="horizontal-checkboxes">', unsafe_allow_html=True)
show_ma_10 = st.checkbox("MA 10", value=True)
show_ma_20 = st.checkbox("MA 20", value=True)
show_ma_50 = st.checkbox("MA 50", value=True)
show_ma_100 = st.checkbox("MA 100", value=True)
show_ma_200 = st.checkbox("MA 200", value=True)
st.markdown('</div>', unsafe_allow_html=True)

if selected_ticker and start_date and end_date:

    # Download stock price data
    stock_data = download_stock_data(selected_ticker, start_date, end_date)

    # Create Candlestick Chart with Moving Averages
    st.plotly_chart(create_candlestick_chart_with_ma(stock_data, show_ma_10, show_ma_20, show_ma_50, show_ma_100, show_ma_200))

    # Fetch news articles data
    news_data = fetch_news_data(selected_ticker)

    # Display news articles if available, else show a message
    st.subheader(f"{selected_ticker} News Articles")
    if len(news_data) > 0:
        for article in news_data:
            st.write(f"Title: {article['headline']}")
            st.write(f"Summary: {article['summary']}")
            st.write(f"URL: {article['url']}")
            st.write("---")
    else:
        st.write(f"No news articles found for {selected_ticker}.")
