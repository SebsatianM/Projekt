import json
import pandas as pd
import matplotlib.pyplot as plt
with open('LINKI2.txt', 'r') as f:
    links = json.loads(f.read())
with open('data/Area.txt', 'r') as f:
    Area = json.loads(f.read())
with open('data/Auction_id.txt', 'r') as f:
    Auction_id = json.loads(f.read())
with open('data/Floor.txt', 'r') as f:
    Floor = json.loads(f.read())
with open('data/Numer_of_floors.txt', 'r') as f:
    Numer_of_floors = json.loads(f.read())
with open('data/Numer_of_rooms.txt', 'r') as f:
    Numer_of_rooms = json.loads(f.read())
with open('data/Price_per_meter.txt', 'r') as f:
    Price_per_meter = json.loads(f.read())
with open('data/Price.txt', 'r') as f:
    Price = json.loads(f.read())

list_of_floats = []

for item in Area:
    pom = item.replace(',','.')
    list_of_floats.append(float(pom.replace(' ','')))



df = pd.DataFrame({
    'Cena':Price,
    'Cena_za_metr:':Price_per_meter,
    'Id':Auction_id,
    'Powierzchnia':list_of_floats,
    'Liczba pokoi':Numer_of_rooms,
    'Liczba pieter': Numer_of_floors,
    'Piętro':Floor
})

print(type(Price[123]))
df[['Cena']].plot(kind='hist',bins=[0.0,200.0,400.0,600.0,800.0,1000.0,1200.0,1400.0,1600.0],rwidth=0.8)
plt.show()()