"""
yahoo finance news web scraper (main_page)

Created on Sun 2021-06-13 20:01:25

@author: Jack.M.Liu
"""

from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

options = Options()
options.add_argument("--disable-notifications")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])

chrome = webdriver.Chrome(executable_path="D:\yahoo_crypto\chromedriver.exe",options=options)
chrome.get("https://finance.yahoo.com/topic/crypto/")
time.sleep(10)

for i in range(20):
    html = chrome.find_element_by_tag_name('html')
    html.send_keys(Keys.END)
    time.sleep(1)

'''
for x in range(1, 30):
    chrome.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(2.5)
'''

time.sleep(5)
soup = BeautifulSoup(chrome.page_source, 'html.parser')
urls=[]
for i in range(1,200):
    try:
        sp=soup.select_one('#Fin-Stream > ul > li:nth-child('+str(i)+') > div > div > div.Ov\(h\).Pend\(44px\).Pstart\(25px\) > h3 > a')
        href="https://finance.yahoo.com"+sp.get('href')
        urls.append(href)
    except:
        pass
    time.sleep(0.2)

#Fin-Stream > ul > li:nth-child(1) > div > div > div.Ov\(h\).Pend\(44px\).Pstart\(25px\) > h3 > a 正常
#Fin-Stream > ul > li:nth-child(3) > div > div > div.Ov\(h\).Pend\(44px\).Pstart\(25px\) > h3 > a 正常

#Fin-Stream > ul > li:nth-child(2) > div > div.Cf.Ov\(h\).Pos\(r\).Py\(14px\).Mt\(-3px\) > div.Ov\(h\).Pend\(44px\) > h3 > a 廣告

