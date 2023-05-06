import streamlit as st
from newsapi import NewsApiClient
from bs4 import BeautifulSoup
import requests

# Initialize NewsAPI client with API key
newsapi = NewsApiClient(api_key='7b36370fdca94d0eba309efc7819b48c')

def search_news(stock_ticker):
    query = stock_ticker + ' 股票 新闻'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    news_links = []
    for url in search(query, num_results=5, lang='zh-CN', pause=2):
        if 'aastocks' in url or 'etnet' in url or 'hkej' in url:
            html = requests.get(url, headers=headers).text
            soup = BeautifulSoup(html, 'html.parser')
            for link in soup.find_all('a', href=True):
                if 'aastocks' in link['href'] or 'etnet' in link['href'] or 'hkej' in link['href']:
                    if len(link['href'].split('?')) > 1:
                        url = link['href'].split('?')[0].split('/url?q=')[1]
                        news_links.append(url)
    news = []
    for link in news_links:
        try:
            article = Article(link)
            article.download()
            article.parse()
            news.append(article.text)
        except:
            continue
    return news

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
