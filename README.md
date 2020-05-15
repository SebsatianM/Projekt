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
- Na dzień 15.05.2020 projekt jest na etapie pisania modułu do analizy i przedstawiana graficznie zebranych danych, wszystkie poprzednie założenia zostały wykonane, oraz zostały podpięte do szkieletu aplikacji żeby wszysktie wcześniejsze kroki mogły wykonywać się automatycznie w zależności od aktualnego stanu posiadanych danych.

# Użyte moduły 
-pandas,
-json,
-lxml,
-BeautifulSoup,
-requests
	
# Napotkane problemy i rozwiązania
- Bardzo długi czas pobierania danych (około 2 godzin) z początu pomogło przejście z BeutifullSoup na lxml natomiast dało to około 10% mniejszy czas natomiast poprzez zastosowanie wielowątkowości czas pobierania skrócił się do około 7 minut czyli dało to około 16 krotne przyspieszenie ponieważ najwięcej czasu było marnowane gdy program czekał na odpowedź z serwera a w tym czasie nic nie robił
- Blokada ze strony serwera, znacznym przyspieszeniu scrapowania czasami serwer blokował dostęp error 403 rozwiązaniem było dodanie randomowego czasu w którym program nic nie robił oraz podczas łączenia użyć sejsi aby serwer "pamiętał" maszynę z której się łączymy,
-Liczne problemy podczas scrapowania min. ogłoszenia które wygasły, brak niektórych zmiennych czy nietypowe przypadki pobieranych zmiennych co powodowało różne długości list z danymi a konsekwencją tego było "rozjeżdżanie" się danych w większości przypadków przypadków pomogł error handling.
