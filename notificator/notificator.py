import smtplib
from utils import get_contacts, read_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def notify():
    email_address = 'projekt.io.git@gmail.com'
    email_password = 'projektio008'

    server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server_ssl.ehlo()
    server_ssl.login(email_address,email_password)

    names, emails =  get_contacts('email_database')
    message_template = read_template('message.txt')
    
    for name, email in zip(names, emails):
        msg = MIMEMultipart()
        
        message = message_template.substitute(PERSON_NAME=name.title())
        
        msg['From'] = email_address
        msg['To'] = email
        msg['Subject'] = "This is test"
        
        msg.attach(MIMEText(message, 'plain'))
        
        server_ssl.send_message(msg)
        
        del msg

notify()