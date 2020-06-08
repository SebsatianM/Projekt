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
    fromaddr= "otodom.notify@gmail.com"
    msg = MIMEMultipart()
    date = datetime.date(datetime.now())
    body = str("Analiza mieszkań we Wrocławiu z dnia {}".format(date))
    if toaddr == "":
        if os.path.basename(os.path.dirname(os.getcwd()))=="DATA":
            os.chdir("../../")
        with open('settings.json', 'r') as f:
            setting_dict = json.loads(f.read())
        globals().update(setting_dict)
        toaddr = email
        try:
            date = datetime.date(datetime.now())
            dirName = "DATA/" + str(date)
            os.chdir(dirName)
            with open('Url_to_email.txt', 'r') as f:
                link_list = f.read().splitlines()
                if len(link_list) > 100:
                    attachment = open("Url_to_email.txt", "rb")
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload((attachment).read())
                    encoders.encode_base64(part)
                    part.add_header(f'Content-Disposition', "attachment; filename=Twoje_linki_{}.txt".format(date))
                    msg.attach(part)
                else:
                   body = str("Analiza mieszkań we Wrocławiu z dnia {}".format(date))
                   for link in link_list:
                       body = body +"\n"+ link
        except FileNotFoundError:
            set_settings.main()
       
    
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Analiza rynku"

    msg.attach(MIMEText(body, 'plain'))

    for img_name in ["Ceny.png", "Liczba.png", "Strefa_rynek.png", "Pokoje_Cena.png"]:
        img_data = open(img_name, 'rb').read()
        image = MIMEImage(img_data, name=os.path.basename(img_name))
        msg.attach(image)


    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "SilneHaslo12345")
    text = msg.as_string()
    
    while True:
        try:
            server.sendmail(fromaddr, toaddr, text)
            break
        except smtplib.SMTPRecipientsRefused:
            print("Nie znaleziono takiego adresu email\nSpróbuj wprowadzić go ponownie!")
            toaddr = input()
    server.quit()


