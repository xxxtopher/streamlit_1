# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 23:56:52 2023

@author: Xtopher
"""

import requests
import json
import pandas as pd
import streamlit as st

headers = {'Content-type': 'application/json'}

# Set the Series ID to CES0000000001 and update the start and end years
data = json.dumps({"seriesid": ['CES0000000001'], "startyear": "2019", "endyear": "2023"})

# Make a POST request to the BLS API
p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)

# Parse the JSON response
json_data = json.loads(p.text)

# Create an empty list to store data
data_list = []

# Iterate through the series and data to extract relevant information
for series in json_data['Results']['series']:
    seriesId = series['seriesID']
    for item in series['data']:
        year = item['year']
        period = item['period']
        value = item['value']
        footnotes = ""
        for footnote in item['footnotes']:
            if footnote:
                footnotes = footnotes + footnote['text'] + ','
        if 'M01' <= period <= 'M12':
            data_list.append([seriesId, year, period, value, footnotes[0:-1]])

# Create a DataFrame from the list
columns = ["series id", "year", "period", "value", "footnotes"]
df = pd.DataFrame(data_list, columns=columns)
df["Date"] = pd.to_datetime(df["year"] + df["period"], format='%YM%m')  # Adjusted format
df = df.sort_values(by="Date")  # Sort DataFrame based on the "Date" column
df = df.set_index('Date')  # Set 'Date' as the index
df["Change in Nonfarm Payrolls"] = df["value"].diff()

# Filter data starting from January 2021
df = df[df.index >= '2021-01-01']

# Convert 'value' column to numeric
df['value'] = pd.to_numeric(df['value'], errors='coerce')

# Streamlit App
st.title("Nonfarm Payrolls Monthly Change")

# Plot the ratio without normalization
st.line_chart(df["Change in Nonfarm Payrolls"])

# Annotate the latest data point
latest_date = df.index[-1]
latest_value = df["Change in Nonfarm Payrolls"].iloc[-1]
st.text(f'Latest Change: {latest_value:.0f}K on {latest_date}')

st.pyplot()  # This line is needed to display Matplotlib plots in Streamlit
