import pandas as pd
import streamlit as st
import plotly.express as px

st.write("Total Deal Value by Type by Industry")

df = pd.read_excel('Data Manipulation Worksheet.xlsx', sheet_name='Financing Table Clean', parse_dates=['DATE'], index_col=['DATE'])
@st.cache
# Manipulate the data
findeals = df.groupby(['TYPE', 'INDUSTRY'])['SIZE'].sum()

fig = px.bar(findeals, x='TYPE', y='SIZE', color='INDUSTRY',
             title='Total Deal Value by Type by Industry')
st.plotly_chart(fig)
