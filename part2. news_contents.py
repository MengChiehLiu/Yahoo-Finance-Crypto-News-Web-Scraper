"""
yahoo finance news web scraper (get_content)

Created on Sun 2021-06-13 20:01:25

@author: Jack.M.Liu
"""

from bs4 import BeautifulSoup
import requests as rq
from datetime import datetime

def get_info(url):
    #send request   
    response = rq.get(url)
    #parse    
    soup = BeautifulSoup(response.text,"lxml")
    #get information we need
    content = soup.find('div', attrs={'class': 'caas-body'}).text
    author = soup.find('span', attrs={'class': 'caas-author-byline-collapse'}).text
    headline = soup.find('h1').text 
    timestamp = datetime.strptime(soup.find('time').text, "%B %d, %Y, %I:%M %p")
    date = timestamp.date()
    time = timestamp.time()
    
    print(headline)
    print(author) 
    print(date)
    print(time)
    print(content) 



url='https://finance.yahoo.com/news/crypto-can-make-the-401k-more-engaging-and-relevant-211848897.html'
get_info(url)