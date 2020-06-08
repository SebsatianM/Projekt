from bs4 import BeautifulSoup as bs
import requests
import itertools
from lxml import html, etree
import json
import lxml 
import concurrent.futures
from math import ceil as round_up
import json
from datetime import datetime
import re
import os
import time
import random
MAX_THREADS = 30    #definiowanie maksymalnej liczby wątków
#inicjalizowanie zmiennych do przechowywania zebranych danych 
links = []
Price_list = []
Price_per_meter_list = []
Auction_id_list = []
error_counter = []
Area_list = []
Number_of_rooms_list = []
Market_list = []
Floor_list = []
Number_of_floors_list = []
URL_list = []
Place_list = []
meh = []
ended_auction = []

session = requests.Session()    #start sesji

def GET_UA():
    """Funkcja która losowo wybiera jednego z User-Agent'a""""
    U_A_List = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",\
                "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36",\
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0"\
                ]
    return random.choice(U_A_List)

def connect():
    """Funkcja do łączenia się z serwerem otodom i szukania ile jest aktualnie ofert i stron z nimi"""
    session.headers.update({'User-Agent':GET_UA()})
    connect = session.get('https://www.otodom.pl/sprzedaz/mieszkanie/wroclaw/?search%5Bcity_id%5D=39&nrAdsPerPage=72')
    soup = bs(connect.text, 'lxml')
    inide_strong_val = soup.find('div', class_="offers-index pull-left text-nowrap")
    offers_number = int(inide_strong_val.find('strong').text.replace(" ",""))
    page_number = round_up(offers_number/72) 
    return page_number,offers_number

def search_links(page_link):
    """Funkcja która dodaje do listy z linkami aukcji linki pobrane z aktualnej strony której adres przyjmuje jako argument""""
    connect_to_courrent_page = session.get(page_link)
    page_soup = bs(connect_to_courrent_page.text, 'lxml')
    auction_headers = page_soup.find_all('header', class_="offer-item-header")
    for x in range(len(auction_headers)):
        if x > 2:
            pom = auction_headers[x].find('a', href=re.compile(r'[/]([a-z]|[A-Z])\w+')).attrs['href']
            links.append(pom)



def page_scrap(URL):
    """Ta funkcja jako argument przyjmuje adres strony na której znajduje się ogłoszenie po czym sprawdza czy jest ono aktualne jeżeli tak to przystępuje wyciągania danych z tego ogłoszenia
    dopisując je do list, jeżeli nie to pomija podany adres i przechodzi dalej """
    
    headers = {'User-Agent':GET_UA()}   #wybieranie losowego User-Agent'a
    page = requests.get(URL, headers=headers) #łączenie się ze stroną 
    os.system("clear")
    print("Odpowiedź z serwera:",page.status_code,"\nIlość przejrzanych ofert:",len(Floor_list))
    if page.status_code == 200: #jeżeli odpowiedź od serwera to 200(czyli wszyskto się udało) wtedy przystępuje do wyciągania danych z ogłoszenia 
        tree = html.fromstring(page.content)    #zmiana otrzymanych danych na element lxml
        try:
            meh.append(tree.xpath('.//div[@class="row-container-query-text"]/text()')[1])   #sprawdzanie czy istnieje div który informuje nas o tym, że aukcja się zakończyła 
            ended_auction.append(URL)
        except:
            try:
                Price_list.append(float(tree.xpath('//div[@class="css-1vr19r7"]/text()')[0][:-3].replace(' ', '').replace(',', '.'))) #pobieranie ceny mieszkania
            except ValueError:
                Price_list.append("")
            try:
                Price_per_meter_list.append(float(tree.xpath('//div[@class="css-zdpt2t"]/text()')[0][:-6].replace(' ', '')))    #pobieranie ceny za metr
            except (IndexError, ValueError):
                Price_per_meter_list.append("")
            try:
                Auction_id_list.append(int(tree.xpath('//div[@class="css-kos6vh"]/text()')[0][20:]))    #pobieranie id ogłoszenia
            except IndexError:
                Auction_id_list.append("")
            try:
                Area = float(tree.xpath('.//div[@class="css-1ci0qpi"]/ul/li[text()="Powierzchnia: "]/strong/text()')[0][:-3])   #pobieranie powierzchni mieszkania /przypadek gdy cena nie zawiera przecinka  
            except ValueError:
                Area = float(tree.xpath('.//div[@class="css-1ci0qpi"]/ul/li[text()="Powierzchnia: "]/strong/text()')[0][:-3].replace(",",".").replace(" ", ""))     #pobieranie powierzchni mieszkania /przypadek gdy cena zawiera przecinek
            except IndexError:
                Area = ""
            try:
                Number_of_rooms = int(tree.xpath('.//div[@class="css-1ci0qpi"]/ul/li[text()="Liczba pokoi: "]/strong/text()')[0])
            except (IndexError,ValueError):
                Number_of_rooms = ""
            try:
                Market = tree.xpath('.//div[@class="css-1ci0qpi"]/ul/li[text()="Rynek: "]/strong/text()')[0].replace("wt\u00f3rny", "wtorny")   #pobieranie z jakiego rynku pochodzi mieszkanie 
            except IndexError:
                Market = ""
            try:
                Floor = float(tree.xpath('.//div[@class="css-1ci0qpi"]/ul/li[text()="Piętro: "]/strong/text()')[0]) #pobieranie piętra na którym znajduje się mieszkanie 
            except (IndexError, ValueError):
                Floor = ""
            try:
                Place = tree.xpath('.//div[@class=" css-0"]/a/text()')  #pobieranie obszaru w kótórym mieszkanie się znajduje 
                Place = Place[0].split(", ")
            except (IndexError, ValueError):
                Place = ""
            try:
                Number_of_floors = int(tree.xpath('.//div[@class="css-1ci0qpi"]/ul/li[text()="Liczba pięter: "]/strong/text()')[0]) #pobieranie liczby pięter budynku w którym dane mieszkanie się znajduje 
            except (IndexError, ValueError):
                Number_of_floors = ""
            try:    #dopisywanie danych z aktualnej strony do list z wcześniejszych stron  
                Area_list.append(Area)
                Number_of_rooms_list.append(Number_of_rooms)
                Market_list.append(Market)
                Floor_list.append(Floor)
                Number_of_floors_list.append(Number_of_floors)
                URL_list.append(URL)
                Place_list.append(Place[1])
            except:
                print("someting goes wrong ¯\_(ツ)_/¯")
    else:
        error_counter.append(URL)   #zapisywanie linków przy których wystapiły problemy podczas pobierania danych
 
def main(story_urls):
    """Funkcja odpowiedzialna za wielowątkowość jako argument przyjmuje listę wszystkich adresów aukcji"""
    threads = min(MAX_THREADS, len(story_urls)) #sprawdzanie czy wcześniej zdefiniowana liczba wątków nie jest większa od liczby wszystkich ogłoszeń 
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:    #asynchroniczne oraz jednoczesne wywoływanie funkcji "page_scrap" z argumentami kolejnych elementów listy "story_urls"
        executor.map(page_scrap, story_urls)

def save_data(file, name):
    """Funkcja która zapisuje dane jak argumenty przyjmuje nazwę zmiennej którą ma zapisać -file, oraz nazwę plkij jak jak ma się nazywać -name"""
    with open(f'{name}.txt', 'wt', encoding='utf#wywołanie funkcji która odpowiada za tworzenie ustawień') as json_file:
        json.dump(file,json_file, ensure_ascii=False)
        
def save():
    """Funkcja która wywołuje funkcję do zapisywania danych"""
    save_data(Area_list,"Area")
    save_data(Auction_id_list,"Auction_id")
    save_data(Floor_list, 'Floor')
    save_data(Number_of_floors_list, 'Number_of_floors')
    save_data(Number_of_rooms_list, 'Number_of_rooms')
    save_data(Price_per_meter_list, 'Price_per_meter')
    save_data(Price_list, 'Price')
    save_data(Market_list, 'Market')
    save_data(URL_list, 'link')
    save_data(Place_list, 'Place')
        

def show_info():
    """Funkcja pomocnicza do wyświeltania ile danych zostało zebranych"""
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
    print(len(Place_list))
    print(len(Place_list))
    print(len(ended_auction))

def init():
    """Główna funkcja odpowiedzialna za odczytanie z pliku wszystkich linków oraz zmierzenie czasu wykonywania funkcji odpowiedzialnej za wielowątkowe pobranie danych"""
    with open('URLs.txt', 'r') as f:
        linki = json.loads(f.read())
    t0 = time.time()
    main(linki)
    t1 = time.time()
    print(f"Pobieranie zajęło {(t1-t0)/60} minut.")         
