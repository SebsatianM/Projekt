import re
import json
def main():
    confirm = 0
    while confirm != 1:
        while True:
            mail = str(input("Wprowadz swojego maila: "))
            if re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", mail):
                break
        while True:
            market = str(input("Wprowadź rynek (wtorny/pierwotny/obojętnie): "))
            if market == "wtorny" or market == "pierwotny" or market == "obojętnie":
                break
        try:
            price_lowest = int(input("Wprowadź minimalną cenę: "))
        except ValueError:
            price_lowest = "Brak danych"
        try:
            price_highest = int(input("Wprowadź maksymalną cenę: "))
        except ValueError:
            price_highest = "Brak danych"
        try:
            rooms_lowest = int(input("Wprowadź minimalną liczbę pokoi: "))
        except ValueError:
            rooms_lowest = "Brak danych"
        try:
            rooms_highest = int(input("Wprowadź maksymalną liczbę pokoi: "))
        except ValueError:
            rooms_highest = "Brak danych"
        try:
            floor_lowest = int(input("Wprowadź najniższe piętro: "))
        except ValueError:
            floor_lowest = "Brak danych"
        try:
            floor_highest = int(input("Wprowadź najwyższe piętro: "))
        except ValueError:
            floor_highest = "Brak danych"
        try:
            area_lowest = int(input("Wprowadź minimalną powierzcnie: "))
        except ValueError:
            area_lowest = "Brak danych"
        try:
            area_highest = int(input("Wprowadź maksymalną powierzchnie: "))
        except ValueError:
            area_highest = "Brak danych"
        
        confirmation = input(f"\nSprawadź dane:\nEmail: {mail}\nRynek: {market}\nCena od: {price_lowest}\nCena do: {price_highest}\nLiczba pokoi od: {rooms_lowest}\nLiczba pokoi do: {rooms_highest}\nPiętro od: {floor_lowest}\nPiętro do: {floor_highest}\nPowierzchnia od: {area_lowest}\nPowierzchnia do: {area_highest}\nPotwierdź [Y/N]: ")
        if confirmation.upper() == "Y":
            confirm = 1

        settings_data = {"email":mail,"market":market, "price_lowest": price_lowest, "price_highest": price_highest,"rooms_lowest":rooms_lowest,"rooms_highest":rooms_highest,"floor_lowest":floor_lowest,"floor_highest":floor_highest,"area_lowest":area_lowest,"area_highest":area_highest}
        with open('settings.json', 'w', encoding='utf8') as json_file:  #zapisywanie otrzymanych danych do pliku z ustawieniami 
            json.dump(settings_data,json_file, ensure_ascii=False)

    