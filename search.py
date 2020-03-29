from bs4 import BeautifulSoup as bs
from bs4 import Comment
import requests
import re
import itertools
from math import ceil as round_up
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'})

connect = session.get('https://www.otodom.pl/sprzedaz/mieszkanie/wroclaw/?search%5Bcity_id%5D=39&nrAdsPerPage=72')
soup = bs(connect.text, 'html.parser')
inide_strong_val = soup.find('div', class_="offers-index pull-left text-nowrap")
offers_number = int(inide_strong_val.find('strong').text.replace(" ",""))
page_number = round_up(offers_number/72) 

def search_links(page_link,links):
    connect_to_courrent_page = session.get(page_link)
    page_soup = bs(connect_to_courrent_page.text, 'html.parser')
    kek = page_soup.find_all('header', class_="offer-item-header")
    for x in range(len(kek)):
        links.append(kek[x].find('a', href = re.compile(r'[/]([a-z]|[A-Z])\w+')).attrs['href'])
    return links
