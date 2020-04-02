from bs4 import BeautifulSoup as bs
from bs4 import Comment
import requests
import re
import itertools
from math import ceil as round_up
links = []
pom = []
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
    for i in range(len(li_list)):
        sublist= li_list[i].text.split(': ')
        if sublist[0] == "Liczba pokoi":
            numer_of_rooms_val = int(sublist[1])
        if sublist[0] == "Liczba pokoi":
            numer_of_rooms_val = int(sublist[1])
        if sublist[0] == "Liczba pokoi":
            numer_of_rooms_val = int(sublist[1])
        if sublist[0] == "Liczba pokoi":
            numer_of_rooms_val = int(sublist[1])        
    print(numer_of_rooms_val)      
    #tmp = li_list[0].text
    #tmp2 = tmp[0:tmp.find(':')]
    #print(tmp2)
    #print(li_list[1].text.split(": ")[1])
def page_phraser_pom(url):
    connect_to_courrent_auction = session.get(url)
    auction_soup = bs(connect_to_courrent_auction.text, 'html.parser')
    auction_prices = auction_soup.find('div', class_="css-9xbh4h")
    price_val = float(auction_prices.find('div', class_="css-1vr19r7").text[:-3].replace(' ', '').replace(',','.'))
    price_per_meter_val = int(auction_prices.find('div', class_="css-zdpt2t").text[:-6].replace(' ', ''))
    auction_id_val = int(auction_soup.find('div', class_="css-kos6vh").text[20:28])
    auction_description = auction_soup.find('div', class_="css-1ci0qpi")
    li_list = auction_description.find_next('ul').find_all('li')
    for i in range(len(li_list)):
        sublist= li_list[i].text.split(': ')
        if sublist[0] == "Rynek":
            rynek_val = sublist[1]
        if sublist[0] == "Piętro":
            numer_of_floor_val = sublist[1]
        if sublist[0] == "Liczba pokoi":
            numer_of_rooms_val = int(sublist[1])
        if sublist[0] == "Liczba pięter":
            condignation_val = int(sublist[1])        
    area_val = float(li_list[0].text.split(": ")[1][:-3].replace(',','.'))
    ogloszenia.append({'Cena:':price_val,'Cena za metr:':price_per_meter_val, 'Numer aukcji:':auction_id_val, 'Powierzchnia:': area_val,'Rynek:':rynek_val,'Liczba pokoi:':numer_of_rooms_val,'Liczba pięter:':condignation_val,'Piętro:':numer_of_floor_val})
    print(len(ogloszenia))
