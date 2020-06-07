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

    img_data1 = open("Ceny.png", 'rb').read()
    image1 = MIMEImage(img_data1, name=os.path.basename("Ceny.png"))

    img_data2 = open("Liczba.png", 'rb').read()
    image2 = MIMEImage(img_data2, name=os.path.basename("Liczba.png"))

    img_data3 = open("Strefa_rynek.png", 'rb').read()
    image3 = MIMEImage(img_data3, name=os.path.basename("Strefa_rynek.jpg"))

    msg.attach(image1)
    msg.attach(image2)
    msg.attach(image3)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "SilneHaslo12345")
    text = msg.as_string()
    try:
        server.sendmail(fromaddr, toaddr, text)
    except smtplib.SMTPRecipientsRefused:
        print("Wprowadzono ")
    server.quit()


