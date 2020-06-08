import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

def read_data(name):
    """Funkcja która przyjmuje jako argument nazwę pliku a zwraca listę z odczytanymi danymi"""
    with open(f'{name}.txt', 'r') as f:
        pom = json.loads(f.read())
    return pom

def main():
    """Funkcja odpowiedzialna za tworzeenie tabeli z danymi oraz oraz na jej podstawie wykresów """
    if not os.path.isfile("out.csv"):   #sprawdzanie czy istnieje plik 'out.csv' w kótrym zapisane są wszysdnie dane połączone ze sobą
        Price = read_data("Price")
        Area = read_data("Area")
        Auction_id = read_data("Auction_id")
        Floor = read_data("Floor")
        Number_of_floors = read_data("Number_of_floors")
        Number_of_rooms = read_data("Number_of_rooms")
        Price_per_meter = read_data("Price_per_meter")
        Market = read_data("Market")
        link = read_data("link")
        Place = read_data("Place")

        df = pd.DataFrame({
            'Cena':Price,
            'Cena_za_metr':Price_per_meter,
            'Id': Auction_id,
            'Rynek': Market,
            'Strefa':Place,
            'Powierzchnia':Area,
            'Liczba pokoi':Number_of_rooms,
            'Liczba pięter': Number_of_floors,
            'Piętro': Floor,
            'URL':link
        }, dtype ='object') #tworzenie zmiennej w której znajdują się wszystkie nasze pobrane dane
        df.to_csv('out.csv', index=False)   #zapisywanie ich w pliku o rozszerzeniu csv
        df = pd.read_csv("out.csv") #odcztanie ich ponownie aby można było na nich pracować, ponieważ bez tego odczytu wcześniej występowały błędy z typami
    else:
        df = pd.read_csv("out.csv")


    df_after_null_price = df.copy() #tworzenie kopii tabeli na której będziemy wykonywać operacje 

    df_after_null_price.drop(['Id','URL'],axis=1, inplace=True) #wyrzucam kolumny URL i Id ponieważ do wykresów nie będą one potrzebne
    df_after_null_price.dropna(subset=["Cena"], inplace=True)   #usuwanie rekordów z tabeli gdziez pusta była tabela 'Cena' 

    df_after_null_price = df_after_null_price.infer_objects()


    pd.set_option('display.float_format', lambda x: '%.2f' % x) #ustawiane formatu zmiennych jako zmienno-przecinkowych

    df_after_null_price = df_after_null_price[df_after_null_price["Powierzchnia"] < 200.0]  #wyrzucanie powierzchni powyżej 1000 m^2
    df_after_null_price = df_after_null_price[df_after_null_price["Cena"] < 2000000.0]  #wyrzucanie ceny powyżej 2 mln
    df_after_null_price = df_after_null_price[df_after_null_price["Liczba pięter"] < 30]  #wyrzucanie powierzchni powyżej 1000 m^2
    for strefa in df_after_null_price["Strefa"].unique():   #usuwanie z naszycha danych strefy w której mamy mniej niż 10 ogłoszeń
        if len(df_after_null_price[df_after_null_price["Strefa"] == strefa]) < 10:
            df_after_null_price = df_after_null_price[df_after_null_price["Strefa"] != strefa]

    sns_strefa_rynek = sns.lmplot(x="Powierzchnia", y="Cena", hue="Rynek", data=df_after_null_price, palette="Set1", height=6, col="Strefa", ci=70) #Tworzenie wykresu zeleżności ceny od powierzch dla poszególnych obszarów
    
    sns_strefa_rynek.savefig("Strefa_rynek.png")    #zapisywanie wykresu 


    columns= ['Cena','Cena_za_metr','Powierzchnia']
    sns_cena_plot = sns.pairplot(df_after_null_price[columns], height=4)    #Tworzenie wykresu zależności wszystkich powierzchni, ceny oraz ceny za metr
    sns_cena_plot.savefig("Ceny.png")
    plt.tight_layout()

    fig, ax = plt.subplots(3,1, figsize=(12,20))     #Tworzenie mapy wykresów
    sns.countplot(df_after_null_price['Liczba pokoi'], ax=ax[0])    #Tworzenie wykresu który zliczają ile jest wszystkich ogłoszeń w zależności od liczy pokoi
    sns.countplot(df_after_null_price['Piętro'], ax=ax[1])  #Tworzenie wykresu który zliczają ile jest wszystkich ogłoszeń w zależności od piętra
    sns.countplot(df_after_null_price['Strefa'], ax=ax[2])  #Tworzenie wykresu który zliczają ile jest wszystkich ogłoszeń w zależności od obszaru w którym się znajdują 
    ax[2].set_xticklabels(ax[2].get_xticklabels(), rotation=50, ha="right") #ustawienie pochyłu opisu osi ostatniego wykresu
    
    fig.savefig("Liczba.png")
    plt.subplots_adjust(left=0.08, bottom=0.1)  #rozmieszczanie położenia wykresów
    plt.figure(figsize=(15, 10))    #ustawianie rozmiaru wykresu 
   
    sns_pokoje = sns.boxplot(x='Liczba pokoi', y='Cena', data=df_after_null_price)  #Tworzenie wykresy pudełkowego na którym można zauważyć rozkład zależności ceny od liczby pokoi 
    sns_pokoje.figure.savefig("Pokoje_Cena.png")

def ploting():
    """Funkcja która odpowiada tylko za pokazywanie""" 
    plt.show()
     
def notification(setting_dict):
    """Funkcja odpowiedzialna za filtrowanie zebranych danych na podstawie ustawień parametrów które otrzymuje jako argument zwraca ona długość listy unikalnych linków czyli ile jest takich ogłoszeń"""
    frame = pd.read_csv("out.csv")
    globals().update(setting_dict)  #zapiswanie do zmiennych globalnych par klucza i wartości ze słownika kótre funkcja otrzymała 
    frame.drop(['Id'],axis=1, inplace=True)
    frame.dropna(subset=["Cena"], inplace=True)

    if market == "wtorny" or market == "pierwotny":
        frame = frame[frame["Rynek"] == market]
    if price_lowest != "Brak danych":
        frame = frame[frame["Cena"] >= price_lowest]
    if price_highest != "Brak danych":
        frame = frame[frame["Cena"] <= price_highest]
    if rooms_lowest != "Brak danych":
        frame.dropna(subset=["Liczba pokoi"], inplace=True)
        frame = frame[frame["Liczba pokoi"] >= rooms_lowest]
    if rooms_highest != "Brak danych":
        frame.dropna(subset=["Liczba pokoi"], inplace=True)
        frame = frame[frame["Liczba pokoi"] <= rooms_highest]
    if floor_lowest != "Brak danych":
        frame.dropna(subset=["Piętro"], inplace=True)
        frame = frame[frame["Piętro"] >= floor_lowest]
    if floor_highest != "Brak danych":
        frame.dropna(subset=["Piętro"], inplace=True)
        frame = frame[frame["Piętro"] <= floor_highest]
    if area_lowest != "Brak danych":
        frame = frame[frame["Powierzchnia"] >= area_lowest]
    if area_highest != "Brak danych":
        frame = frame[frame["Powierzchnia"] <= area_highest]

    selected_urls = frame["URL"].unique()   #Tworzenie listy unikalnych linków z pozostałych danych
    
    outF = open('Url_to_email.txt', "w")
    for line in selected_urls:
    #zapisywanie listy unikalnych linków do pliku linia po lini
        outF.write(line)
        outF.write("\n")
    outF.close()
    return len(frame["URL"].unique())
    
def print_info():
    """Funkcja służąca do sprawdzania długości danych """
    print("Cena:", len(Price))
    print("Cena za metr:", len(Price_per_meter))
    print("Id:", len(Auction_id))
    print("Powierzchnia:", len(Area))
    print("Liczba pokoi:",len(Number_of_rooms))    
    print("Liczba pieter:", len(Number_of_floors))
    print("Pietro:", len(Floor))
    print("Strefa:", len(Place))    
        
