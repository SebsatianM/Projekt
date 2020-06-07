import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
import os
def send_charts(toaddr):

    fromaddr= "otodom.notify@gmail.com"
    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Analiza rynku"

    from datetime import datetime
    date = datetime.date(datetime.now())

    body = str("Analiza mieszkań we Wrocławiu z dnia {}".format(date))

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


