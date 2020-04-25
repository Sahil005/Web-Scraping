#!/usr/bin/env python
# coding: utf-8

# In[9]:


##GAADI.COM 
from lxml import html
import requests
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


page = requests.get('https://www.gaadi.com/store-locator')
tree = html.fromstring(page.content)

ls=[]

for num in range(0,100):    
    store_name = tree.xpath('//*[@id="sellCar11"]/div/div/div/div[1]/div[2]/ul/li['+str(num)+']/div/div[2]/div[1]/text()') 
    store_loc = tree.xpath('//*[@id="sellCar11"]/div/div/div/div[1]/div[2]/ul/li['+str(num)+']/div/div[2]/div[2]/text()')
    store_latlng = tree.xpath('//*[@id="sellCar11"]/div/div/div/div[1]/div[2]/ul/li['+str(num)+']/div/div[2]/a/@href')
    ls.append([store_name,store_loc,store_latlng])
ls1 = [x for x in ls if x != [[],[],[]]]


gaadi = pd.DataFrame(ls1)
gaadi = gaadi.rename(columns={0:'name',1:'address',2:'google_map_url'})
gaadi['name'] = gaadi.apply(lambda row:row['name'][0],axis=1)
gaadi['address'] = gaadi.apply(lambda row:row['address'][0],axis=1)
gaadi['google_map_url'] = gaadi.apply(lambda row:row['google_map_url'][0],axis=1)


# In[22]:


## OLX(CASH MY CAR)
page1 = requests.get('https://www.cashmycar.olx.in/locations')
tree1 = html.fromstring(page1.content)
cities_ls =[]
for num in range(0,200):
    cities = tree1.xpath('/html/body/div[1]/div/div/div[1]/div['+str(num)+']/div/text()')
    cities[0] = cities[0].replace(' ','-') #cities with 2 name parts like 'New Delhi' are seperated with - on the site
    cities_ls.append(cities)
	
ls=[]
for items in cities_ls:    
    page2 = requests.get('https://www.cashmycar.olx.in/locations/'+str(items[0].lower())+'/')
    tree2 = html.fromstring(page2.content)
    for num in range(0,30):
        store_name_cmc = tree2.xpath('/html/body/div[1]/div/div/div[1]/div['+str(num)+']/div/div[1]/text()')
        store_loc_cmc = tree2.xpath('/html/body/div[1]/div/div/div[1]/div['+str(num)+']/div/div[2]/text()')
        ls.append([store_name_cmc,store_loc_cmc])
ls1 = [x for x in ls if x != [[],[]]]

olx = pd.DataFrame(ls1)
olx = olx.rename(columns={0:'name',1:'address'})
olx['name'] = olx.apply(lambda row:row['name'][0],axis=1)
olx['address'] = olx.apply(lambda row:row['address'][0],axis=1)
print(olx)

