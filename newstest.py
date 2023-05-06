import streamlit as st
from newsapi import NewsApiClient
from bs4 import BeautifulSoup
import requests

# Initialize NewsAPI client with API key
newsapi = NewsApiClient(api_key='7b36370fdca94d0eba309efc7819b48c')

def search_news(stock_ticker):
    # Search for news articles using NewsAPI
    news = newsapi.get_everything(q=stock_ticker, language='zh')
    articles = news['articles']
    
    # Scrape news articles from Chinese finance news websites
    sites = ['aastocks.com', 'etnet.com', 'hkej.com']
    for site in sites:
        search_url = f"https://www.google.com/search?q={stock_ticker}+site%3A{site}&rlz=1C1GCEU_zh-CNHK832HK832&oq={stock_ticker}+site%3A{site}"
        res = requests.get(search_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select('.kCrYT a')
        for i, link in enumerate(links):
            if site in link['href']:
                url = link['href'].split('?')[0].split('/url?q=')[1]
                res = requests.get(url)
                soup = BeautifulSoup(res.text, 'html.parser')
                content = soup.select('p')
                news_content = ''
                for c in content:
                    news_content += c.text
                articles.append({'title': link.text, 'description': news_content, 'url': url})
    
    return articles

# Define Streamlit app
st.title('Stock News Search')
st.write('This app searches for news articles related to a stock ticker.')
stock_ticker = st.text_input('Enter a stock ticker (e.g. AAPL)')

if st.button('Search'):
    # Search for news articles
    news = search_news(stock_ticker)
    
    # Display news articles in a table
    st.write(f'Showing news articles for {stock_ticker}:')
    for article in news:
        st.write('---')
        st.write(article['title'])
        st.write(article['description'])
        st.write(article['url'])
