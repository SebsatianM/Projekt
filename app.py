import search
import charts
import emails
import set_settings
import pandas as pd
import os 
import json
from datetime import datetime
import re

date = datetime.date(datetime.now()) #data w formacie YYYY-MM-DD
dirName = "DATA/" + str(date) #ścieżka do aktualnego foldert roboczy
page_number = search.connect()[0] #liczba wyszstkich stron z ofertami
total_offerts_number = search.connect()[1] #liczba wszystkich ofert

def next_step(url):
    """Funkcja która odpowiada za prawidłową kolejność wywoływania funkcji"""
    try:
        with open('Area.txt', 'r') as f:
            pom = json.loads(f.read())
            if len(url) - len(pom) > 300: #sprawdzanie czy liczba linków kóre zostały porane zbyt znacząco nie różni się od liczby pobranych danych
                search.init() #wywoałanie funkcji która zarządza porcesem pobierania danych na podstawie wcześniej zebranych linków
                search.save() #wywołanie funkcji do zapisu danych 
    except FileNotFoundError:
        search.init()
        search.save()
    charts.main() #wywołanie funkcji do analizy danych oraz do tworzenia wykresów 

    while True:
        """Pętla do obsługi interakcji z użytkownikiem"""
        while True:
            """Pętla do wprowadzania instrukcji od użytkownika"""
            action = input("Wpisz co chcesz zrobić:\n(0).Wyświetl wykresy \n(1).Jednorazowo wyślij wykresy na maila\n(2).Wyślij interesujące Cię ogłoszenia maila\n(3).Edytuj swoje ustawienia\n(4).Wyjdź\n")
            try:
                action = int(action)
                if (0 <= action <= 4):
                    break
                print ("\nWybrałeś błędną operacje")
            except ValueError:
                print("\nWprowadź liczbę!")

        if action == 0: #przypadek gdy użytkownik wybrał opcję 0
            charts.ploting()    #wywołanie funkcji która pokazyje stowrzone wcześniej wykresy
            
        elif action == 1:   #przypadek gdy użytkownik wybrał opcję 0
            while True:
                email_adr = str(input("Wprowadz swojego maila: "))
                if re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email_adr): #walidacja adresu email
                    break
            emails.send_charts(email_adr)   #wywoływanie funkcji do wysyłania maili z adresem podanym przy jednorazowym wysyłaniu danych 

        elif action == 2:   #przypadek gdy użytkownik wybrał opcję 2
            if os.path.basename(os.path.dirname(os.getcwd()))=="DATA":  #sprawdzanie w jakim folderze się znajdujemy
                os.chdir("../../")
            try:
                with open('settings.json', 'r+') as f:  #próba otwarcia pliku z ustawieniami 
                    s = json.loads(f.read())
                    os.chdir(os.getcwd() + "/DATA/" + str(date))    #zmiana folderu
                    print("Ilość pasujących aukcji:", charts.notification(s))   #wywołanie funkcji która zwraca liczbę ogłoszeń które pasują do naszych ustawień                   
                    send_val = input("Wysłać ogłoszenia na maila?? [Y/N]: ")                    
                    if send_val.upper() == "Y":
                       emails.send_charts() #wywołanie funkcji która wysyła maila    
            except FileNotFoundError:   #sytuacja gdy nie znajdziemy pliku z ustawieniami 
                set_settings.main() #wywołanie funkcji która odpowiada za tworzenie ustawień
                with open('settings.json', 'r+') as f: #ponowna prób otwarcia stworzonego wcześniej pliku
                    s = json.loads(f.read())
                    os.chdir(os.getcwd() + "/DATA/" + str(date))
                    print("Ilość pasujących aukcji:", charts.notification(s))                    
                    send_val = input("Wysłać ogłoszenia na maila?? [Y/N]: ")                    
                    if send_val.upper() == "Y":
                        emails.send_charts()
                           
        elif action == 3:   #przypadek gdy użytkownik wybrał opcję 3
            if os.path.basename(os.path.dirname(os.getcwd()))=="DATA":
                os.chdir("../../")
            set_settings.main() #wywołanie funkcji która odpowiada za tworzenie ustawień
        elif action == 4:
            break
        os.system("clear")


def collecting_links():
    """Funkcja która łączy się z Otodom oraz 'przechodzi' przez wszysktie strony z ogłoszeniami i wyciąga z nich adresy wszystkich ogłoszeń""""
    for page_num in range(page_number+1):
        search.search_links('https://www.otodom.pl/sprzedaz/mieszkanie/wroclaw/?search%5Bcity_id%5D=39&nrAdsPerPage=72&page=' + str(page_num))
        os.system("clear")
        print("Pobieranie danych na dzień:{}".format(date))
        print("Pobiernie linków:",round((len(search.links)/total_offerts_number)*100),"%")
    links = search.links
    with open('URLs.txt', 'w') as f:
        f.write(json.dumps(links))
    next_step(links)

"""Sprawdzanie czy istnieje folder do przechowywania danych jeżeli nie to go toworzy jeżeli tak to sprawdza czy dzisiaj już dane były pobierane"""
if not os.path.exists(dirName):
    os.makedirs(dirName)
    os.chdir(os.getcwd() + "/DATA/" + str(date))
    collecting_links()
else:   
    os.chdir(os.getcwd() + "/DATA/" + str(date))
    try:
        with open('URLs.txt', 'r') as f:
            linki = json.loads(f.read())
    except FileNotFoundError:
        collecting_links()
        try:
            with open('URLs.txt', 'r') as f:
                linki = json.loads(f.read())
        except FileNotFoundError: 
            collecting_links()
    if len(linki) - total_offerts_number > 100: 
        collecting_links()
    else:
        next_step(linki)

