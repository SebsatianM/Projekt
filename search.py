from bs4 import BeautifulSoup as bs
from bs4 import Comment
import requests
import re
import itertools
from math import ceil as round_up
import json
import pandas as pd
import matplotlib.pyplot as plt
links = []
Price = []
Price_per_meter = []
Auction_id = []
Area = []
Market = []
Numer_of_rooms = []
Numer_of_floors = []
Floor = []
ogloszenia = []

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'})
connect = session.get('https://www.otodom.pl/sprzedaz/mieszkanie/wroclaw/?search%5Bcity_id%5D=39&nrAdsPerPage=72')
soup = bs(connect.text, 'html.parser')
inide_strong_val = soup.find('div', class_="offers-index pull-left text-nowrap")
offers_number = int(inide_strong_val.find('strong').text.replace(" ",""))
page_number = round_up(offers_number/72) 

def search_links(page_link):
    connect_to_courrent_page = session.get(page_link)
    page_soup = bs(connect_to_courrent_page.text, 'html.parser')
    auction_headers = page_soup.find_all('header', class_="offer-item-header")
    for x in range(len(auction_headers)):
        if x > 2:
            links.append(auction_headers[x].find('a', href = re.compile(r'[/]([a-z]|[A-Z])\w+')).attrs['href'])

def page_phraser(url):
    connect_to_courrent_auction = session.get(url)
    auction_soup = bs(connect_to_courrent_auction.text, 'html.parser')
    auction_descriptio = auction_soup.find('div', class_="css-1ci0qpi")
    li_list = auction_descriptio.find_next('ul').find_all('li')
    for rynek in range(len(li_list)):
        sublist= li_list[i].text.split(': ')
        if sublist[0] == "Liczba pokoi":
            try:
                Numer_of_rooms.append(int(sublist[1]))
            except:
                Numer_of_rooms.append("Brak danych") 
        if sublist[0] == "Liczba pokoi":
            numer_of_rooms_val = int(sublist[1])
        if sublist[0] == "Liczba pokoi":
            numer_of_rooms_val = int(sublist[1])
        if sublist[0] == "Liczba pokoi":
            numer_of_rooms_val = int(sublist[1])        
    print(numer_of_rooms_val)      

def page_phraser_pom(url):
    sublist = []
    try:
        connect_to_courrent_auction = session.get(url)
        auction_soup = bs(connect_to_courrent_auction.text, "lxml")
        auction_prices = auction_soup.find('div', class_="css-9xbh4h")
    
        Price.append(float(auction_prices.find('div', class_="css-1vr19r7").text[:-3].replace(' ', '').replace(',', '.')))
        Price_per_meter.append(int(auction_prices.find('div', class_="css-zdpt2t").text[:-6].replace(' ', '')))
        Auction_id.append(int(auction_soup.find('div', class_="css-kos6vh").text[20:28]))
        auction_description = auction_soup.find('div', class_="css-1ci0qpi")
        li_list = auction_description.find_next('ul').find_all('li')

        for i in range(len(li_list)):
            sublist.append(li_list[i].text.split(': '))
        flat_list = [item for sublist2 in sublist for item in sublist2]
        if "Powierzchnia" in flat_list:
            Area.append(float(flat_list[flat_list.index("Powierzchnia")+1][:-3].replace(',','.'))) 
        else:
            Area.append("Brak danych")
        if "Liczba pokoi" in flat_list:
            Numer_of_rooms.append(flat_list[flat_list.index("Liczba pokoi")+1]) 
        else:
            Numer_of_rooms.append("Brak danych")
        if "Rynek" in flat_list:
            Market.append(flat_list[flat_list.index("Rynek")+1]) 
        else:
            Market.append("Brak danych")
        if "Piętro" in flat_list:
            Floor.append(flat_list[flat_list.index("Piętro")+1]) 
        else:
            Floor.append("Brak danych")
        if "Liczba pięter" in flat_list:
            Numer_of_floors.append(flat_list[flat_list.index("Liczba pięter")+1]) 
        else:
            Numer_of_floors.append("Brak danych")
        #print(f"Collecting auction data: {round((len(Price) / len(links)) * 100,1) }%")
        print(len(Price))
    except:
        print("ogłoszenie wygasło")
        

    
with open('LINKI2.txt', 'r') as f:
    links = json.loads(f.read())
for x in links[:10]:
    page_phraser_pom(x)

with open('data2/Price.txt', 'w') as f:
    f.write(json.dumps(Price))
    
with open('data2/Price_per_meter.txt', 'w') as f:
    f.write(json.dumps(Price_per_meter))
with open('data2/Auction_id.txt', 'w') as f:
    f.write(json.dumps(Auction_id))
with open('data2/Area.txt', 'w') as f:
    f.write(json.dumps(Area))

with open('data2/Numer_of_rooms.txt', 'w') as f:
    f.write(json.dumps(Numer_of_rooms))
with open('data2/Numer_of_floors.txt', 'w') as f:
    f.write(json.dumps(Numer_of_floors))
with open('data2/Floor.txt', 'w') as f:
    f.write(json.dumps(Floor))
 
    
