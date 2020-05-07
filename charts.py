import json
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
def read_data(name):
    with open(f'{name}.txt', 'r') as f:
        pom = json.loads(f.read())
    return pom
date = datetime.date(datetime.now())
os.chdir("DATA/"+str(date))
Price = read_data("Price")
Area = read_data("Area")
Auction_id = read_data("Auction_id")
Floor = read_data("Floor")
Number_of_floors = read_data("Number_of_floors")
Number_of_rooms = read_data("Number_of_rooms")
Price_per_meter = read_data("Price_per_meter")
URL = read_data("URLs")
print(len(URL))
def print_info():
    print("Cena:", len(Price))
    print("Cena za metr:", len(Price_per_meter))
    print("Id:", len(Auction_id))
    print("Powierzchnia:", len(Area))
    print("Liczba pokoi:",len(Number_of_rooms))    
    print("Liczba pieter:", len(Number_of_floors))
    print("Pietro:", len(Floor))
        

df = pd.DataFrame({
    'Cena':Price,
    'Cena_za_metr':Price_per_meter,
    'Id':Auction_id,
    'Powierzchnia':Area,
    'Liczba pokoi':Number_of_rooms,
    'Liczba pięter': Number_of_floors,
    'Piętro': Floor,
    'URL':URL
})

print(df[df["Liczba pięter"]==50])