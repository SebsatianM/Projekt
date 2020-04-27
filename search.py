from bs4 import BeautifulSoup as bs
from bs4 import Comment
import requests
import itertools
from math import ceil as round_up
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import re
import os
import timeit
links = []
Price = []
Price_per_meter = []
Auction_id = []
Area = []
Market = []
Number_of_rooms = []
Number_of_floors = []
Floor = []
ogloszenia = []

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'})
connect = session.get('https://www.otodom.pl/sprzedaz/mieszkanie/wroclaw/?search%5Bcity_id%5D=39&nrAdsPerPage=72')
soup = bs(connect.text, 'lxml')
inide_strong_val = soup.find('div', class_="offers-index pull-left text-nowrap")
offers_number = int(inide_strong_val.find('strong').text.replace(" ",""))
page_number = round_up(offers_number/72) 

print(page_number)
def search_links(page_link):
    connect_to_courrent_page = session.get(page_link)
    page_soup = bs(connect_to_courrent_page.text, 'lxml')
    auction_headers = page_soup.find_all('header', class_="offer-item-header")
    for x in range(len(auction_headers)):
        if x > 2:
            pom = auction_headers[x].find('a', href=re.compile(r'[/]([a-z]|[A-Z])\w+')).attrs['href']
            print(pom[29:])
            links.append(pom[29:])


def page_phraser(url):
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
            Number_of_rooms.append(int(flat_list[flat_list.index("Liczba pokoi")+1])) 
        else:
            Number_of_rooms.append("Brak danych")
        if "Rynek" in flat_list:
            Market.append(flat_list[flat_list.index("Rynek")+1]) 
        else:
            Market.append("Brak danych") 
        if "Piętro" in flat_list:
            if flat_list[flat_list.index("Piętro") + 1] == "parter":
                Floor.append(0)
            elif flat_list[flat_list.index("Piętro") + 1] == "poddasze": 
                Floor.append(99)    
            else:
                Floor.append(int(flat_list[flat_list.index("Piętro") + 1]))
        else:
            Floor.append("Brak danych")
        if "Liczba pięter" in flat_list:
            Number_of_floors.append(int(flat_list[flat_list.index("Liczba pięter")+1])) 
        else:
            Number_of_floors.append("Brak danych")
        os.system("clear")
        print(f"Collecting auction data: {round((len(Price) / len(links)) * 100,1) }%")
        print(len(Floor))
    except:
        os.system("clear")
        print("ogłoszenie wygasło")
        


def save_data(file, name):
    with open(f'{name}.txt', 'w') as f:
        f.write(json.dumps(file))
        
def save():
    save_data(Area,"Area")
    save_data(Auction_id,"Auction_id")
    save_data(Floor, 'Floor')
    save_data(Number_of_floors, 'Number_of_floors')
    save_data(Number_of_rooms, 'Number_of_rooms')
    save_data(Price_per_meter, 'Price_per_meter')
    save_data(Price, 'Price')
