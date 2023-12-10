import requests
import json
import pandas as pd
import streamlit as st

df = pd.read_csv('hourly_earnings_data.csv')

# Streamlit App
st.title("Nonfarm Payrolls Monthly Change")

# Plot the ratio with 'Date' as the x-axis
st.line_chart(df.set_index('Date')["Change in Nonfarm Payrolls"], use_container_width=True)

# Annotate the latest data point
latest_date = df.index[-1]
latest_value = df["Change in Nonfarm Payrolls"].iloc[-1]
st.text(f'Latest Change: {latest_value:.0f}K on {latest_date}')

st.pyplot()  # This line is needed to display Matplotlib plots in Streamlit

st.set_option('deprecation.showPyplotGlobalUse', False)



