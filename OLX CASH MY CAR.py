#!/usr/bin/env python
# coding: utf-8

# In[1]:


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

