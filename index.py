import requests
from bs4 import BeautifulSoup
import urllib
import re

def getLinks(url):
    html_page = urllib.urlopen(url)
    soup = BeautifulSoup(html_page)
    links = []

    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        links.append(link.get('href'))

    return links

print( getLinks("https://arstechnica.com") )