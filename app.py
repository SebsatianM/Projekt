import search
links = []
import pandas as pd
import os 

for page_num in range(search.page_number+1):
    search.search_links('https://www.otodom.pl/sprzedaz/mieszkanie/wroclaw/?search%5Bcity_id%5D=39&nrAdsPerPage=72&page=' + str(page_num), links)
    os.system()
    print("Collecting auction URLs:",round((len(links)/search.offers_number)*100),"%")
    print(len(links))
