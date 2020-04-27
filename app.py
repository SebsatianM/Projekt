import search
pom = []
import pandas as pd
import os 
import json
from datetime import datetime
date = datetime.date(datetime.now())
print(os.getcwd())
for page_num in range(search.page_number+1):
    search.search_links('https://www.otodom.pl/sprzedaz/mieszkanie/wroclaw/?search%5Bcity_id%5D=39&nrAdsPerPage=72&page=' + str(page_num))
    os.system("clear")
    print("Pobieranie danych na dzień:{}".format(date))
    print("Collecting auction URLs:",round((len(search.links)/search.offers_number)*100),"%")
links = search.links
print(len(links))
dirName = "DATA/"+str(date)
if not os.path.exists(dirName):
    os.makedirs(dirName)
    os.chdir(os.getcwd() + "/DATA/" + str(date))
else:   
    os.chdir(os.getcwd() + "/DATA/" + str(date))
with open('URLs.txt', 'w') as f:
    f.write(json.dumps(links))

#search.get_data()
#search.save()