import smtplib
import set_settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import os
import json
from datetime import datetime

def send_charts(toaddr=""):
    """Funkcja która odpowiada za wysyłanie maili na podany adres który jest argumentem funkcji domyślnie jest on pusty aby można było skorzystać z adresu zapisanego w ustawieniach"""
    fromaddr= "otodom.notify@gmail.com" #adres z którego zostanie wysłany email
    msg = MIMEMultipart()   #incjalizacja szkieletu wiadomości  
    date = datetime.date(datetime.now())    #pobranie aktualnej daty    
    body = str("Analiza mieszkań we Wrocławiu z dnia {}".format(date))  #stworzenie treści maila 
    if toaddr == "":    #przypadek w którym wywołujemy funkcję bez argumentu 
        if os.path.basename(os.path.dirname(os.getcwd()))=="DATA":  #sprawdzanie w jakim folderze się znajdujemy 
            os.chdir("../../")
        with open('settings.json', 'r') as f:   #otwieranie plku z ustawieniami 
            setting_dict = json.loads(f.read())
        globals().update(setting_dict)  #zapiswanie do zmiennych globalnych par klucza i wartości ze słownika kótre funkcja otrzymała 
        toaddr = email  #przypisanie adresu z ustawień jako adred odbiorcy maila 
        try:
            date = datetime.date(datetime.now())
            dirName = "DATA/" + str(date)
            os.chdir(dirName)
            with open('Url_to_email.txt', 'r') as f:    #odczytanie pliku z 'interesującymi nas ofertami'
                link_list = f.read().splitlines()  
                if len(link_list) > 100:    #przypadek gdy lista ta jest dłuższa niż 100 wtedy linki są wysyłąne w pliku
                    attachment = open("Url_to_email.txt", "rb")
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload((attachment).read())
                    encoders.encode_base64(part)
                    part.add_header(f'Content-Disposition', "attachment; filename=Twoje_linki_{}.txt".format(date))
                    msg.attach(part)    #dodawanie załącznika w formie tekstowej
                else:   #gdy lista  z 'interesującymi nas ofertami' jest mniejsza niż 100 wtedy linki są wysyłane w treści maila
                   body = str("Analiza mieszkań we Wrocławiu z dnia {}".format(date))
                   for link in link_list:
                       body = body +"\n"+ link
        except FileNotFoundError:
            set_settings.main()
       
    
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Analiza rynku"    #ustawianie tytułu maila 

    msg.attach(MIMEText(body, 'plain')) #dodawania treści maila

    for img_name in ["Ceny.png", "Liczba.png", "Strefa_rynek.png", "Pokoje_Cena.png"]:  #pętla do dodawania załączników w formacie png
        img_data = open(img_name, 'rb').read()
        image = MIMEImage(img_data, name=os.path.basename(img_name))
        msg.attach(image)


    server = smtplib.SMTP('smtp.gmail.com', 587)    #połączenie się z serwerem SMTP poczty gmail
    server.starttls()   #włącznie połącznia tunelowanego
    server.login(fromaddr, "SilneHaslo12345")   #logowanie się na adres z którego zostanie wysłana wiadomość
    text = msg.as_string()  #zmiana naszej wiadomości na tekst
    
    while True:
        #pętla która będzie próbowała wysłać maila na podany adres w przypadku gdy adres nie będzie się zgadzał poprosi jego ponowne wpisanie 
        try:
            server.sendmail(fromaddr, toaddr, text)
            break
        except smtplib.SMTPRecipientsRefused:
            print("Nie znaleziono takiego adresu email\nSpróbuj wprowadzić go ponownie!")
            toaddr = input()
    server.quit()   #zakończenie połącznie z serwerem 


