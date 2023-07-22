import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta
import streamlit as st
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
    fig.update_layout(title=f"{selected_ticker} Candlestick Chart",
                      xaxis_title="Date",
                      yaxis_title="Price",
                      height=600,
                      paper_bgcolor='black',  # Set background color to black
                      plot_bgcolor='black',   # Set plot background color to black
                      xaxis_rangeslider_visible=True,
                      xaxis_rangeslider_thickness=0.1,
                      xaxis_rangeslider_bgcolor='rgba(30,30,30,0.4)',
                      xaxis_rangeslider_bordercolor='grey',
                      xaxis_rangeslider_borderwidth=1,
                      xaxis_rangeslider_borderpad=5,
                      xaxis_rangeselector=dict(
                          buttons=list([
                              dict(count=1, label="1M", step="month", stepmode="backward"),
                              dict(count=6, label="6M", step="month", stepmode="backward"),
                              dict(count=1, label="YTD", step="year", stepmode="todate"),
                              dict(count=1, label="1Y", step="year", stepmode="backward"),
                              dict(step="all")
                          ])
                      )
                      )

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

# Custom CSS to set the background color to black
st.markdown(
    """
    <style>
    body {
        background-color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main Streamlit app
st.set_page_config(page_title="Stock Analysis Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide", 
                   initial_sidebar_state="collapsed")

st.title("Stock Analysis Dashboard")

# Get user input for stock ticker and date range
selected_ticker = st.text_input("Enter stock ticker (e.g. AAPL):")

# Get the current date
current_date = datetime.now()

# Set the default end date to the current date
end_date = st.date_input("Enter end date:", current_date)

# Set the default start date to one year before the end date
default_start_date = current_date - timedelta(days=365)
start_date = st.date_input("Enter start date:", default_start_date)

if selected_ticker and start_date and end_date:

    # Download stock price data
    stock_data = download_stock_data(selected_ticker, start_date, end_date)

    # Create Candlestick Chart
    st.plotly_chart(create_candlestick_chart(stock_data))

    # Fetch news articles data
    news_data = fetch_news_data(selected_ticker)

    # Display news articles if available, else show a message
    st.subheader(f"{selected_ticker} News Articles")
    if len(news_data) > 0:
        for article in reversed(news_data):  # Display news in reverse chronological order
            st.markdown(f"**Title:** {article['headline']}")  # Make news title bold
            st.write(f"Date: {article['datetime']}")
            st.write(f"Summary: {article['summary']}")
            st.write(f"URL: {article['url']}")
            st.write("---")
    else:
        st.write(f"No news articles found for {selected_ticker}.")
