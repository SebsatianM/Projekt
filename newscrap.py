import time
import requests
from lxml import html, etree
import lxml 
import json
import os
import concurrent.futures
import re
Price_list = []
Price_per_meter_list = []
Auction_id_list = []
error_counter = []
MAX_THREADS = 25
Area_list = []
Number_of_rooms_list = []
Market_list = []
Floor_list = []
Number_of_floors_list = []
URL_list = []
meh = []
ended_auction = []
header = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0"}
def page_scrap(URL):
    """Ta funkcja jako argument przyjmuje adres strony na której znajduje się ogłoszenie po czym sprawdza czy jest ono aktualne jeżeli tak to przystępuje wyciągania danych z tego ogłoszenia
    dopisując je do list, jeżeli nie to pomija podany adres i przechodzi dalej"""
    
    page = requests.get(URL, headers=header)
    os.system("clear")
    print(page.status_code)
    print(len(Floor_list))
    if page.status_code == 200:
        tree = html.fromstring(page.content)
        try:
            meh.append(tree.xpath('.//div[@class="row-container-query-text"]/text()')[1])
            ended_auction.append(URL)
        except:
            try:
                Price_list.append(float(tree.xpath('//div[@class="css-1vr19r7"]/text()')[0][:-3].replace(' ', '').replace(',', '.')))
            except ValueError:
                Price_list.append("Brak danych")
            try:
                Price_per_meter_list.append(float(tree.xpath('//div[@class="css-zdpt2t"]/text()')[0][:-6].replace(' ', '')))
            except (IndexError, ValueError):
                Price_per_meter_list.append("Brak danych")
            try:
                Auction_id_list.append(int(tree.xpath('//div[@class="css-kos6vh"]/text()')[0][20:]))
            except IndexError:
                  Auction_id_list.append("Brak danych")
            try:
                Area = float(tree.xpath('.//div[@class="css-1ci0qpi"]/ul/li[text()="Powierzchnia: "]/strong/text()')[0][:-3])
            except ValueError:
                Area = float(tree.xpath('.//div[@class="css-1ci0qpi"]/ul/li[text()="Powierzchnia: "]/strong/text()')[0][:-3].replace(",",".").replace(" ", ""))
            except IndexError:
                Area = "Brak danych"
            try:
                Number_of_rooms = int(tree.xpath('.//div[@class="css-1ci0qpi"]/ul/li[text()="Liczba pokoi: "]/strong/text()')[0])
            except (IndexError,ValueError):
                Number_of_rooms = "Brak danych"
            try:
                Market = tree.xpath('.//div[@class="css-1ci0qpi"]/ul/li[text()="Rynek: "]/strong/text()')[0].replace("wt\u00f3rny", "wtorny")
              
            except IndexError:
                Market = "Brak danych"
            try:
                Floor = float(tree.xpath('.//div[@class="css-1ci0qpi"]/ul/li[text()="Piętro: "]/strong/text()')[0])
            except (IndexError, ValueError):
                Floor = "Brak danych"
            try:
                Number_of_floors = int(tree.xpath('.//div[@class="css-1ci0qpi"]/ul/li[text()="Liczba pięter: "]/strong/text()')[0])
            except (IndexError, ValueError):
                Number_of_floors = "Brak danych"
            try:
                Area_list.append(Area)
                Number_of_rooms_list.append(Number_of_rooms)
                Market_list.append(Market)
                Floor_list.append(Floor)
                Number_of_floors_list.append(Number_of_floors)
                URL_list.append("https://www.otodom.pl/oferta/"+URL)
            except:
                print("sometinh goes wrong ¯\_(ツ)_/¯")
    else:
        error_counter.append(URL)
    timeout = 0.22
    time.sleep(timeout)
 
def download_stories(story_urls):
    threads = min(MAX_THREADS, len(story_urls))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(page_scrap, story_urls)

def main(story_urls):
    t0 = time.time()
    download_stories(story_urls)
    t1 = time.time()
    print(f"{(t1-t0)/60} minutes to download {len(linki)} stories.")         
  
y = []

os.chdir("DATA/2020-05-07")
with open('URLs.txt', 'r') as f:
    linki = json.loads(f.read())
for x in linki:
    y.append("https://www.otodom.pl/oferta/" + x)
main(y[:200])

def save_data(file, name):
    with open(f'{name}.txt', 'w') as f:
        f.write(json.dumps(file))
        
def save():
    save_data(Area_list,"Area")
    save_data(Auction_id_list,"Auction_id")
    save_data(Floor_list, 'Floor')
    save_data(Number_of_floors_list, 'Number_of_floors')
    save_data(Number_of_rooms_list, 'Number_of_rooms')
    save_data(Price_per_meter_list, 'Price_per_meter')
    save_data(Price_list, 'Price')
    save_data(Market_list, 'Market')
    save_data(URL_list, 'link')
save()
print(len(meh))
print(len(Price_list))
print(len(Price_per_meter_list))
print(len(Auction_id_list))
print(len(error_counter))
print(len(Area_list))
print(len(Auction_id_list))
print(len(Floor_list))
print(len(Number_of_rooms_list))
print(len(Number_of_floors_list))
print(ended_auction)
