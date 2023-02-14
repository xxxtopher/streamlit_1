import pandas as pd
import streamlit as st

st.write("APP WORKING!")

tickers = ['AAPL', 'MSFT', 'NFLX']
ticker = st.selectbox("Pick a ticker",tickers)

df = pd.read_csv(ticker + ".csv", parse_dates=['Date'], index_col=['Date'])

st.write(df)