import search

pom = []
import pandas as pd
import os 
import json
from datetime import datetime
date = datetime.date(datetime.now())

page_number = search.connect()[0]
total_offerts_number = search.connect()[1]

def next_step(url):
    print("mamy to")
    print(len(url))
    search.download_stories(url)
    search.save()
    search.show_info()

def collecting_links():
    for page_num in range(page_number+1):
        search.search_links('https://www.otodom.pl/sprzedaz/mieszkanie/wroclaw/?search%5Bcity_id%5D=39&nrAdsPerPage=72&page=' + str(page_num))
        os.system("clear")
        print("Pobieranie danych na dzień:{}".format(date))
        print("Collecting auction URLs:",round((len(search.links)/total_offerts_number)*100),"%")
    links = search.links
    with open('URLs.txt', 'w') as f:
        f.write(json.dumps(links))
    next_step(links)


dirName = "DATA/" + str(date)
if not os.path.exists(dirName):
    os.makedirs(dirName)
    os.chdir(os.getcwd() + "/DATA/" + str(date))
    collecting_links()
else:   
    os.chdir(os.getcwd() + "/DATA/" + str(date))
    try:
        with open('URLs.txt', 'r') as f:
            linki = json.loads(f.read())
            print(len(linki))
            print(total_offerts_number)
            print(len(linki) - total_offerts_number)
    except FileNotFoundError:
        collecting_links()
        try:
            with open('URLs.txt', 'r') as f:
                linki = json.loads(f.read())
        except FileNotFoundError:
            collecting_links()
    if len(linki) - total_offerts_number < -10:
        collecting_links()
    else:
        next_step(linki)

