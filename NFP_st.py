import requests
import json
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Assuming the 'hourly_earnings_data.csv' file has a 'Date' column
df = pd.read_csv('hourly_earnings_data.csv')
df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' to datetime if it's not already

# Streamlit App
st.title("Nonfarm Payrolls Monthly Change")

# Plot the ratio with 'Date' as the x-axis
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df['Date'], df['Change in Nonfarm Payrolls'])

# Annotate the latest data point
latest_date = df['Date'].iloc[-1]
latest_value = df["Change in Nonfarm Payrolls"].iloc[-1]
ax.annotate(f'Latest Change: {latest_value:.0f}K on {latest_date}',
            xy=(latest_date, latest_value),
            xytext=(20, 30),
            textcoords='offset points',
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"),
            fontsize=12)

# Format x-axis as dates
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.xticks(rotation=45)

# Display the plot
st.pyplot(fig)

st.set_option('deprecation.showPyplotGlobalUse', False)



