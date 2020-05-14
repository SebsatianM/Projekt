import json
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
def read_data(name):
    with open(f'{name}.txt', 'r') as f:
        pom = json.loads(f.read())
    return pom
Price = read_data("Price")
Area = read_data("Area")
Auction_id = read_data("Auction_id")
Floor = read_data("Floor")
Number_of_floors = read_data("Number_of_floors")
Number_of_rooms = read_data("Number_of_rooms")
Price_per_meter = read_data("Price_per_meter")
Market = read_data("Market")
link = read_data("link")


def print_info():
    print("Cena:", len(Price))
    print("Cena za metr:", len(Price_per_meter))
    print("Id:", len(Auction_id))
    print("Powierzchnia:", len(Area))
    print("Liczba pokoi:",len(Number_of_rooms))    
    print("Liczba pieter:", len(Number_of_floors))
    print("Pietro:", len(Floor))
        
print(link[869])
print(link[2646])
df = pd.DataFrame({
    'Cena':Price,
    'Cena_za_metr':Price_per_meter,
    'Id': Auction_id,
    'Rynek':Market,
    'Powierzchnia':Area,
    'Liczba pokoi':Number_of_rooms,
    'Liczba pięter': Number_of_floors,
    'Piętro': Floor,
    'URL':link
})
df.to_excel('out.xlsx',index=False)
print(df[df["Liczba pięter"]==5].count(level="Cena"))