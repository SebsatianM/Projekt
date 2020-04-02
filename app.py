import search
pom = []
import pandas as pd
import os 

for page_num in range(search.page_number+1):
    search.search_links('https://www.otodom.pl/sprzedaz/mieszkanie/wroclaw/?search%5Bcity_id%5D=39&nrAdsPerPage=72&page=' + str(page_num))
    os.system('clear')
    print("Collecting auction URLs:",round((len(search.links)/search.offers_number)*100),"%")
links = search.links

for auction_url in links:
    search.page_phraser_pom(auction_url)
   