import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def whats_on_the_news(ticker):
    
    ##using datetime to build the name of the csv file
    now = datetime.now()
    now_string = now.strftime("%Y%m%d%H%M%S")
    
    ## getting the ticker from yfinance
    T = yf.Ticker(ticker)
    news = T.news

    ##Creating a list to populate with titles articles, links and associated companies
    rows = []

        ##creating a for loop to go through 
    for article in news:

        ##yfinance data
        title = article['title']
        link = article['link']
        associated_companies = article['relatedTickers']   

        ##data extracted through requests
        r = requests.get(link, timeout=2.50)
        status = r.status_code == requests.codes.ok
        soup = BeautifulSoup(r.text,'html.parser')

        ##Some articles don't provide any content so we create the below try - except will return a blank
        ##cell if article doesn't provide data
        try:
            art = soup.find('meta', {'name': 'description'})
            content = art['content']
        except TypeError:
            content=None

        ##appending to list
        rows.append([title, content, link, associated_companies])
        
    ##creating the dataframe and appending the gathered data
    dfnews = pd.DataFrame(rows, columns=['title', 'article', 'link','associated_companies'])
    dfnews.to_csv(f'{str(ticker)}_news_{now_string}.csv')
    ##returning a dataframe
    return dfnews