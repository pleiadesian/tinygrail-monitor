# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 09:43:16 2019

@author: allegra
"""

from selenium import webdriver
import json
import pandas as pd
import time

characterId=21368

driver = webdriver.Chrome(r"/Users/pro/Downloads/chromedriver")
ids=pd.read_excel('宫内莲华.xlsx')['bgmid'].values
nickNames=pd.read_excel('宫内莲华.xlsx')['昵称'].values

asklist2=[]
bidlist2=[]
c=0
for i in ids:
    driver.get("https://www.tinygrail.com/api/chara/user/{characterId}/{userId}".format(characterId=characterId,userId=str(i)))
    j=driver.find_element_by_xpath('/html/body/pre').text
    d=json.loads(j)
    askRecord2=d['Value']['Asks']
    bidRecord2=d['Value']['Bids']
    if askRecord2:
        asklist2.append([i,nickNames[c],[k['Begin'] for k in askRecord2], [k['Price'] for k in askRecord2], [k['Amount'] for k in askRecord2]])
    if bidRecord2:
        bidlist2.append([i,nickNames[c],[k['Begin'] for k in bidRecord2], [k['Price'] for k in bidRecord2], [k['Amount'] for k in bidRecord2]])
    c+=1
    time.sleep(1)
    
driver.quit()
#
ask2=pd.DataFrame(asklist2)
bid2=pd.DataFrame(bidlist2)

ask2.to_excel('ask2.xlsx',index=False,header=['id','Nickname','begin time','price','amount'])
bid2.to_excel('bid2.xlsx',index=False,header=['id','Nickname','begin time','price','amount'])