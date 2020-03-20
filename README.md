# Projekt
Projekt w języku skryptowym

W tym projekcie chcę stworzyć min. analizę rynku nieruchomości we Wrocławiu w tym celu dane będę wyciągał z serwisu Otodom,
dane które chcę pobierać to cena, metrarz, cena za m^2, liczba pokoi, piętro na którym znajduje się mieszkanie 
oraz inne dodatkowe informacje zawarte w ogłoszeniu

Dodatkowo chcę stowrzyć newsletter który będzie informował mnie o nowych ogłoszeniach spełniających moje oczekiwania wobec szukanego mieszkania


Lista zadań do wykonania:
- połącznie się ze stroną
- pobranie ze strony linków wszystkich ogłoszeń,
- przejście kolejno przez wszystkie ogłoszenia,
- wydobycie niezbędnych informacji z ogłoszeń,
- zapisanie wydobytych informacji,
- analiza zebranych danych,
- przedstawienie ich w sensowny sposób,
- porównanie informacji (z aktualnej analizy) z informacjami (z poprzedniej analizy), //w momencie gdy wykonujemy ją kolejny raz
- stworzenie listy ogłoszeń w których cena uległa zmianie oraz listy nowych ogłoszeń,
- poinformowanie użytkownika o nowych ofertach oraz o tych w których cena się zmieniła,

# Status


# Użyte moduły 
-Selenium
	
# Napotkane problemy i rozwiązania
-'selenium.common.exceptions.WebDriverException: Message: 'geckodriver' executable needs to be in PATH.' rozwiązanie to skopiowanie pliku 'geckodriver' do /usr/local/bin poleceniem 'sudo cp geckodriver /usr/local/bin'