import pandas as pd
import streamlit as st

st.write("APP WORKING!")

tickers = ['AAPL', 'GE', 'NKE']
ticker = st.selectbox("Pick a ticker",tickers)

df = pd.read_csv(ticker + ".csv", parse_dates=['Date'], index_col=['Date'])

begDate = df.index.min()
endDate = df.index.max()

minDateDropdown = pd.to_datetime('2010-01-01')

pickStart = st.date_input("Pick start date", begDate)
pickEnd = st.date_input("Pick end date:", endDate)

filterDF = df.loc[pickStart:pickEnd]

st.write(filterDF)

import plotly.express as px
fig = px.line(filterDF, x=filterDF.index, y="Close")
st.plotly_chart(fig)

st.write(begDate)
st.write(endDate)

