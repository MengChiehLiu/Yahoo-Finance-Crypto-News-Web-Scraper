"""
yahoo finance news web scraper

Created on Sun 2021-06-13 20:01:25

@author: Jack.M.Liu
"""

import pandas as pd
import requests as rq
from bs4 import BeautifulSoup
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

options = Options()
options.add_argument("--disable-notifications")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])

chrome = webdriver.Chrome(executable_path="D:\yahoo_crypto\chromedriver.exe",options=options) #executable_path
chrome.get("https://finance.yahoo.com/topic/crypto/")
time.sleep(10)

for i in range(20):
    html = chrome.find_element_by_tag_name('html')
    html.send_keys(Keys.END)
    time.sleep(1)

time.sleep(3)
soup = BeautifulSoup(chrome.page_source, 'html.parser')
urls=[]


for i in range(1,200):
    try:
        sp=soup.select_one('#Fin-Stream > ul > li:nth-child('+str(i)+') > div > div > div.Ov\(h\).Pend\(44px\).Pstart\(25px\) > h3 > a')
        href="https://finance.yahoo.com"+sp.get('href')
        urls.append(href)
    except:
        pass
    print('\r' + '[URLs Scraping]:[%s%s]%.2f%%;' % ('█' * int(i*20/200), ' ' * (20-int(i*20/200)),float(i/200*100)), end='')
    time.sleep(0.2)

def get_news(url):
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
    t = timestamp.time()
    time.sleep(0.2)
    return date, t, author, headline, content

df=pd.DataFrame()
dates=[]
times=[]
authors=[]
headlines=[]
contents=[]

percent=0
total=len(urls)
for i in urls:
    try:
        date, t, author, headline, content = get_news(i)
        dates.append(date)
        times.append(t)
        authors.append(author)
        headlines.append(headline)
        contents.append(content)
    except:
        pass
    percent+=1
    print('\r' + '[News Scraping]:[%s%s]%.2f%%;' % ('█' * int(percent*20/total), ' ' * (20-int(percent*20/total)),float(percent/total*100)), end='')

df["date"]=dates
df["time"]=times
df["author"]=authors
df["headline"]=headlines
df["content"]=contents
df.to_csv('yahoo finance news.csv')

