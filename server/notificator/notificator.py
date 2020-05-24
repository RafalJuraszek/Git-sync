import smtplib
from utils import read_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../db')
from database_handler import EmailsDatabaseHandler


def notify():
    email_address = 'projekt.io.git@gmail.com'
    email_password = 'projektio008'
    database = EmailsDatabaseHandler()
    #tymczasowo, tutaj ni bedzie zadnego tworzenia
    database.create_email_table()
    database.insert_data('rafaljuraszek@interia.pl', 'rafal')

    server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server_ssl.ehlo()
    server_ssl.login(email_address,email_password)

    emails, names =  database.get_data()
    message_template = read_template('message.txt')
    database.close()
    
    for email, name in zip(emails, names):
        msg = MIMEMultipart()
        
        message = message_template.substitute(PERSON_NAME=name.title())
        
        msg['From'] = email_address
        msg['To'] = email
        msg['Subject'] = "This is test"
        
        msg.attach(MIMEText(message, 'plain'))
        
        server_ssl.send_message(msg)
        
        del msg

notify()