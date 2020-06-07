import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

def read_data(name):
    with open(f'{name}.txt', 'r') as f:
        pom = json.loads(f.read())
    return pom

def main():
    if not os.path.isfile("out.csv"):
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
        }, dtype ='object')
        df.to_csv('out.csv', index=False)
        df = pd.read_csv("out.csv")
    else:
        df = pd.read_csv("out.csv")


    df_after_null_price = df.copy()

    df_after_null_price.drop(['Id','URL'],axis=1, inplace=True) #wyrzucam kolumny URL i Id ponieważ do wykresów nie będą one potrzebne
    df_after_null_price.dropna(subset=["Cena"], inplace=True)

    df_after_null_price = df_after_null_price.infer_objects()


    pd.set_option('display.float_format', lambda x: '%.2f' % x)

    df_after_null_price = df_after_null_price[df_after_null_price["Powierzchnia"] < 200.0]  #wyrzucanie powierzchni powyżej 1000 m^2
    df_after_null_price = df_after_null_price[df_after_null_price["Cena"] < 2000000.0]  #wyrzucanie ceny powyżej 2 mln
    df_after_null_price = df_after_null_price[df_after_null_price["Liczba pięter"] < 30]  #wyrzucanie powierzchni powyżej 1000 m^2
    for strefa in df_after_null_price["Strefa"].unique():   #usuwanie z naszycha danych strefy w której mamy mniej niż 10 ogłoszeń
        if len(df_after_null_price[df_after_null_price["Strefa"] == strefa]) < 10:
            df_after_null_price = df_after_null_price[df_after_null_price["Strefa"] != strefa]

    sns_strefa_rynek = sns.lmplot(x="Powierzchnia", y="Cena", hue="Rynek", data=df_after_null_price, palette="Set1", height=6, col="Strefa", ci=70)
    
    sns_strefa_rynek.savefig("Strefa_rynek.png")


    columns= ['Cena','Cena_za_metr','Powierzchnia']
    sns_cena_plot = sns.pairplot(df_after_null_price[columns], height=4)
    sns_cena_plot.savefig("Ceny.png")
    plt.tight_layout()

    fig, ax = plt.subplots(3,1, figsize=(12,20))
    sns.countplot(df_after_null_price['Liczba pokoi'], ax=ax[0])
    sns.countplot(df_after_null_price['Piętro'], ax=ax[1])
    sns.countplot(df_after_null_price['Strefa'], ax=ax[2])
    ax[2].set_xticklabels(ax[2].get_xticklabels(), rotation=50, ha="right")
    


    fig.savefig("Liczba.png")
    plt.subplots_adjust(left=0.08, bottom=0.1)
    plt.figure(figsize=(15, 10))
   
    sns_pokoje = sns.boxplot(x='Liczba pokoi', y='Cena', data=df_after_null_price)
    sns_pokoje.figure.savefig("Pokoje_Cena.png")

def ploting():  
    plt.show()
     
def notification(setting_dict):
    frame = pd.read_csv("out.csv")
    locals().update(setting_dict)
    frame.drop(['Id'],axis=1, inplace=True) #wyrzucam kolumny URL i Id ponieważ do wykresów nie będą one potrzebne
    frame.dropna(subset=["Cena"], inplace=True)
    print(market)
    if market == "obojętnie":
        print("")
    else:
        frame = frame[frame["Market"] == market]
    if price_lowest != "Brak danych":
        frame = frame[frame["Cena"]> price_lowest]
        
def print_info():
    print("Cena:", len(Price))
    print("Cena za metr:", len(Price_per_meter))
    print("Id:", len(Auction_id))
    print("Powierzchnia:", len(Area))
    print("Liczba pokoi:",len(Number_of_rooms))    
    print("Liczba pieter:", len(Number_of_floors))
    print("Pietro:", len(Floor))
    print("Strefa:", len(Place))    
        
