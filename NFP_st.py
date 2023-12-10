import requests
import json
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Assuming the 'hourly_earnings_data.csv' file has a 'Date' column
df = pd.read_csv('hourly_earnings_data.csv')
df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' to datetime if it's not already

# Additional checks
print("Data Types:")
print(df.dtypes)

print("\nDataFrame:")
print(df)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDataFrame Shape:")
print(df.shape)

# Streamlit App
st.title("Nonfarm Payrolls Monthly Change")

# Plot the ratio with 'Date' as the x-axis
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df['Date'], df['Change in Nonfarm Payrolls'])

# Format x-axis as dates
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.xticks(rotation=45)

# Display the plot
st.pyplot(fig)



