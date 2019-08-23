import json
import pandas as pd
import os
from selenium import webdriver
import time

class Grail(object):
    def __init__(self, char_id, char_name, flag=0):
        brower_path = r"/Users/pro/Downloads/chromedriver"
        driver = webdriver.Chrome(brower_path)
        self.char_id = char_id
        self.char_name = char_name
        self.driver = driver
        self.flag = flag
      
    def get_shds(self):
        char_id = self.char_id
        char_name = self.char_name
        driver = self.driver
        
        driver.get("https://www.tinygrail.com/api/chara/users/"+char_id+"/1/1000")
        j = driver.find_element_by_xpath('/html/body/pre').text
        d = json.loads(s=j)

        shareholders = d['Value']['Items']
        shareholderNames = [i['Name'] for i in shareholders]
        shareholderNicknames = [i['Nickname'] for i in shareholders]

        bgmids = []
        for i in shareholderNames:
            driver.get('http://api.bgm.tv/user/'+i)
            j = driver.find_element_by_xpath('/html/body/pre').text
            d = json.loads(s=j)
            bgmids.append(d['id'])

        inventory = []
        for i in bgmids:
            driver.get(
                'https://www.tinygrail.com/api/chara/user/assets/'+str(i)+'/true')
            j = driver.find_element_by_xpath('/html/body/pre').text
            d = json.loads(s=j)
            characters = d['Value']['Characters']
            for character in characters:
                if character['Name'] == char_name:
                    inventory.append(character['State'])
            time.sleep(1)

        l = [
            ('https://bgm.tv/user/'+str(bgmid), bgmid, name, ivt)
            for bgmid, name, ivt in zip(bgmids, shareholderNicknames, inventory)
        ]

        df = pd.DataFrame(l, columns=['个人主页', 'bgmid', '昵称', '持仓数'])
        save_path = "./"+char_name+"_shds.xlsx"
        df.to_excel(save_path, index=False)
        # display(df)
        return save_path
        
    def get_pendings(self):

        char_id = self.char_id
        char_name = self.char_name
        driver = self.driver
        flag = self.flag
        shds_path = "./" + char_name + "_shds.xlsx"
        if not os.path.isfile(shds_path) or flag == 1:
            shds_path = self.get_shds()
        
        df_shds = pd.read_excel(shds_path)
        ids = df_shds['bgmid'].values
        nickNames = df_shds['昵称'].values
        asks = []
        bids = []

        for c, i in enumerate(ids):
            driver.get("https://www.tinygrail.com/api/chara/user/{characterId}/{userId}".format(
                characterId=char_id, userId=str(i)))
            j = driver.find_element_by_xpath('/html/body/pre').text
            d = json.loads(j)

            ask_rec = d['Value']['Asks']
            bid_rec = d['Value']['Bids']

            if ask_rec:
                asks += [('ask', i, nickNames[c], k['Begin'], k['Price'], k['Amount'])
                         for k in ask_rec]
            if bid_rec:
                bids += [('bid', i, nickNames[c], k['Begin'], k['Price'], k['Amount'])
                         for k in bid_rec]
            time.sleep(1)
        df_ask = pd.DataFrame(asks, columns=['Pending', 'id', 'Nickname', 'begin time', 'price', 'amount'])
        df_bid = pd.DataFrame(bids, columns=['Pending', 'id', 'Nickname', 'begin time', 'price', 'amount'])
        df_ask.set_index(['Pending', 'id', 'Nickname', 'begin time'], inplace=True)
        df_bid.set_index(['Pending', 'id', 'Nickname', 'begin time'], inplace=True)
        df_ab = pd.concat([df_ask,df_bid]).sort_values(['price'], ascending=False)
        # display(df_ab)
        save_path = './'+ char_name + '_pending.xlsx'
        df_ab.to_excel(save_path, index=True)
        return save_path


char_id = "21368"
char_name = "宫内莲华"

shds_flag = 0
pending_flag = 0
grail = Grail(char_id, char_name, flag=pending_flag)

# shds_path = "./" + char_name + "_shds.xlsx"
#
# # get shareholders table
# if not os.path.isfile(shds_path) or shds_flag == 1:
#     shds_path = grail.get_shds()

pending_path = "./" + char_name + "_pending.xlsx"

# get pendings
if not os.path.isfile(pending_path) or shds_flag == 1 or pending_flag == 1:
    pending_path = grail.get_pendings()

