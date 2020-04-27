import time
import requests
from lxml import html
import json
import os
import concurrent.futures
Price_list = []
Price_per_meter_list = []
Auction_id_list = []
error_counter = []
MAX_THREADS = 30

def page_scrap(URL):
    page = requests.get(URL)
    if page.status_code == 200:
        tree = html.fromstring(page.content)
        try:
            Price_list.append(float(tree.xpath('//div[@class="css-1vr19r7"]/text()')[0][:-3].replace(' ', '').replace(',', '.')))
        except ValueError:
            Price_list.append("Brak danych")
        try:
            Price_per_meter_list.append(float(tree.xpath('//div[@class="css-zdpt2t"]/text()')[0][:-6].replace(' ', '')))
        except IndexError:
            Price_per_meter_list.append("Brak danych")
        Auction_id_list.append(str(tree.xpath('//div[@class="css-kos6vh"]/text()')[0][20:]))
        try:
            description = tree.find('.//div[@class="css-1ci0qpi"]')
        except:    
            print("brah")
        print(str(description)
        print(len(Price_list))
        #print(Price_per_mete_list[0])
        print(Auction_id_list[0])
    else:
        error_counter.append(URL)
def download_stories(story_urls):
    threads = min(MAX_THREADS, len(story_urls))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(page_scrap, story_urls)

def main(story_urls):
    t0 = time.time()
    download_stories(story_urls)
    t1 = time.time()
    print(f"{(t1-t0)/60} minutes to download {len(linki)} stories.")         
    #print(len(Price_list))
    #print(len(Price_per_meter_list))
    #print(len(Auction_id_list))
y= []
os.chdir("DATA/2020-04-27")
with open('URLs.txt', 'r') as f:
    linki = json.loads(f.read())
for x in linki:
    y.append("https://www.otodom.pl/oferta/" + x)
    #print("https://www.otodom.pl/oferta/"+x)
#main(y)
page_scrap('https://www.otodom.pl/oferta/rezydencja-szczodra-s4-dom-w-najlepszej-cenie-ID41nUj.html')
print(len(Price_list))
print(len(Price_per_meter_list))
print(len(Auction_id_list))
print(len(error_counter))
