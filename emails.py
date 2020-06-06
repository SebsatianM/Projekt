import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

fromaddr= "otodom.notify@gmail.com"
toaddr ="seba5211@wp.pl"

msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Analiza rynku"

from datetime import datetime
date = datetime.date(datetime.now())

body = str("Analiza z dnia {}".format(date))

msg.attach(MIMEText(body, 'plain'))

filename1 = "Ceny.png"
attachment1 = open("DATA/{}/Ceny.png".format(date), "rb")
filename2 = "Liczba.png"
attachment2 = open("DATA/{}/Liczba.png".format(date), "rb")
filename3 = "Strefa_rynek.png"
attachment3 = open("DATA/{}/Strefa_rynek.png".format(date), "rb")

part1 = MIMEBase('application', 'octet-stream')
part2 = MIMEBase('application', 'octet-stream')
part3 = MIMEBase('application', 'octet-stream')

part1.set_payload((attachment1).read())
encoders.encode_base64(part1)
part1.add_header('Content-Disposition', "attachment; filename= %s" % filename1)

part2.set_payload((attachment2).read())
encoders.encode_base64(part2)
part2.add_header('Content-Disposition', "attachment; filename= %s" % filename2)

part3.set_payload((attachment3).read())
encoders.encode_base64(part3)
part3.add_header('Content-Disposition', "attachment; filename= %s" % filename3)

msg.attach(part1)
msg.attach(part2)
msg.attach(part3)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "SilneHaslo12345")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()


