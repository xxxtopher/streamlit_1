import pandas as pd
import streamlit as st
import plotly.express as px

st.write("Total Deal Value by Type by Industry")

@st.cache
pick = st.sidebar.radio('Pick a chart type',('Bar','Box & Whisker','Sunburst','Tree Map'))

findeals = pd.read_excel('Data Manipulation Worksheet.xlsx', sheet_name='Financing Table Clean')
dfColumns = list(findeals.columns)
if pick=="Bar" or pick=="Box & Whisker":

    xCat = st.sidebar.selectbox("Pick a category for the x-axis",dfColumns,index=dfColumns.index("TYPE"))
    zCat = st.sidebar.selectbox("Pick a category for the legend filter",dfColumns,index=dfColumns.index("TYPE"))
    hover = st.sidebar.selectbox("Pick a category for the hover",dfColumns,index=dfColumns.index("ISSUER"))
    
    custTitle = "Total Deal Value by " + xCat.title() + " by " + zCat.title()

    if pick=="Bar":
        fig = px.bar(findeals,
                     x=xCat,
                     y='SIZE',
                     color=zCat,hover_name=hover,
                    title=custTitle)
    else:
        fig = px.box(findeals,
                 x=xCat,
                 y='SIZE',
                 hover_name=hover,
                 color=zCat,
                title=custTitle)
    st.plotly_chart(fig)

elif pick=="Sunburst" or pick=="Tree Map":
    
    l1 = st.sidebar.selectbox("Pick a category for first layer",dfColumns,index=dfColumns.index("INDUSTRY"))
    l2 = st.sidebar.selectbox("Pick a category for second layer",dfColumns,index=dfColumns.index("TYPE"))
    l3 = st.sidebar.selectbox("Pick a category for third layer",dfColumns,index=dfColumns.index("LEAD UNDERWRITER"))
    l4 = st.sidebar.selectbox("Pick a category for fourth layer",dfColumns,index=dfColumns.index("ISSUER"))
    
    if pick=="Sunburst":
        fig = px.sunburst(findeals, path=[l1, l2, l3,l4], values='SIZE')
    else:
        fig = px.treemap(findeals, path=[l1, l2, l3,l4], values='SIZE')

st.plotly_chart(fig)
