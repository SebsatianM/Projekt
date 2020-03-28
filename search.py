from bs4 import BeautifulSoup as bs
import requests
import re
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'})

def search_links(page_link,links):
    connect_to_courrent_page = session.get(page_link)
    html_soup = bs(connect_to_courrent_page.text, 'html.parser')
    kek = html_soup.find_all('header', class_="offer-item-header")

    for x in range(len(kek)):
        links.append(kek[x].find('a', href = re.compile(r'[/]([a-z]|[A-Z])\w+')).attrs['href'])
    return links
