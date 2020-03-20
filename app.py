from selenium import webdriver
from selenium.webdriver.common import keys
import time
class Otodombot:
    def __init__(self, nazwa, haslo):
        self.nazwa = nazwa
        self.haslo = haslo
        self.bot = webdriver.Firefox()
    
    def login(self):
        bot = self.bot
        bot.get('https://www.otodom.pl/')
        time.sleep(3)

kek = Otodombot('seba5211@wp.pl', 'adassd')
kek.login()