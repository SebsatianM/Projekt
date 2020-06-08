import search
import charts
import emails
import set_settings
import pandas as pd
import os 
import json
from datetime import datetime
import re

date = datetime.date(datetime.now())
dirName = "DATA/" + str(date)
page_number = search.connect()[0]
total_offerts_number = search.connect()[1]

def next_step(url):
    try:
        with open('Area.txt', 'r') as f:
            pom = json.loads(f.read())
            if len(url) - len(pom) > 300:
                search.init()
                search.save()
    except FileNotFoundError:
        search.init()
        search.save()
    charts.main()

    while True:
        while True:
            action = input("Wpisz co chcesz zrobić:\n(0).Wyświetl wykresy \n(1).Jednorazowo wyślij wykresy na maila\n(2).Wyślij interesujące Cię ogłoszenia maila\n(3).Edytuj swoje ustawienia\n(4).Wyjdź\n")
            try:
                action = int(action)
                if (0 <= action <= 5):
                    break
                print ("\nWybrałeś błędną operacje")
            except ValueError:
                print("\nWprowadź liczbę!")

        if action == 0:
            charts.ploting()
            exit_val = input("Wyjść? [Y/N]: ")
            if exit_val.upper() == "Y":
                break

        elif action == 1:
            while True:
                email_adr = str(input("Wprowadz swojego maila: "))
                if re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email_adr):
                    break
            emails.send_charts(email_adr)

        elif action == 2:
            if os.path.basename(os.path.dirname(os.getcwd()))=="DATA":
                os.chdir("../../")
            try:
                with open('settings.json', 'r+') as f:
                    s = json.loads(f.read())
                    os.chdir(os.getcwd() + "/DATA/" + str(date))
                    print("Ilość pasujących aukcji:", charts.notification(s))                    
                    send_val = input("Wysłać ogłoszenia na maila?? [Y/N]: ")                    
                    if send_val.upper() == "Y":
                       emails.send_charts()       
            except FileNotFoundError:
                set_settings.main()
                with open('settings.json', 'r+') as f:
                    s = json.loads(f.read())
                    os.chdir(os.getcwd() + "/DATA/" + str(date))
                    print("Ilość pasujących aukcji:", charts.notification(s))                    
                    send_val = input("Wysłać ogłoszenia na maila?? [Y/N]: ")                    
                    if send_val.upper() == "Y":
                        emails.send_charts()              
        elif action == 3:
            if os.path.basename(os.path.dirname(os.getcwd()))=="DATA":
                os.chdir("../../")
            set_settings.main()
        elif action == 4:
            break
        os.system("clear")


def collecting_links():
    for page_num in range(page_number+1):
        search.search_links('https://www.otodom.pl/sprzedaz/mieszkanie/wroclaw/?search%5Bcity_id%5D=39&nrAdsPerPage=72&page=' + str(page_num))
        os.system("clear")
        print("Pobieranie danych na dzień:{}".format(date))
        print("Pobiernie linków:",round((len(search.links)/total_offerts_number)*100),"%")
    links = search.links
    with open('URLs.txt', 'w') as f:
        f.write(json.dumps(links))
    next_step(links)


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

