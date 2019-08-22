# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 03:48:32 2019

@author: allegra
"""

from selenium import webdriver
import json
import pandas as pd

characterId=21368

driver = webdriver.Chrome(r"/Users/pro/Downloads/chromedriver")
ids=pd.read_excel('宫内莲华.xlsx')['bgmid'].values

asklist=[]
bidlist=[]
for i in ids:
    driver.get("https://www.tinygrail.com/api/chara/user/{characterId}/{userId}".format(characterId=characterId,userId=str(i)))
    j=driver.find_element_by_xpath('/html/body/pre').text
    d=json.loads(j)
    askRecord=d['Value']['AskHistory']
    bidRecord=d['Value']['BidHistory']
    if askRecord:
        asklist.append([i,[k['TradeTime'] for k in askRecord], [k['Price'] for k in askRecord], [k['Amount'] for k in askRecord]])
    if bidRecord:
        bidlist.append([i,[k['TradeTime'] for k in bidRecord], [k['Price'] for k in bidRecord], [k['Amount'] for k in bidRecord]])


driver.quit()

ask=pd.DataFrame(asklist)
bid=pd.DataFrame(bidlist)

ask.to_csv("ask.csv")
bid.to_csv("bid.csv")
