import smtplib
from server.notificator.utils import read_template, ready_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
from server.scrapper.scrapper import Scrapper


# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../db')
from server.db.database_handler import EmailsDatabaseHandler, ReposDatabaseHandler


def notify(master_repo_id):
    email_address = 'projekt.io.git@gmail.com'
    email_password = 'projektio008'
    database = EmailsDatabaseHandler()
    # tymczasowo, tutaj ni bedzie zadnego tworzenia
    # database.create_email_table()
    # database.insert_data('rafaljuraszek@interia.pl', 'rafal', 'Git-sync')
    # potrzeba jeszcze jakie repo
    server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server_ssl.ehlo()
    server_ssl.login(email_address, email_password)

    print("notify debug 2")
    repos_db = ReposDatabaseHandler()
    url = repos_db.get_master_repo_url(master_repo_id)
    repos_db.close()
    print("url -> " + url)
    s = Scrapper(repo_url= url, master_repo_id = master_repo_id)
    s.scrap_associated()


    # emails, names, repos =  database.get_data()

    # dla konretnego repo
    emails, names = database.get_data_where_master_repo(master_repo_id)

    message_template = ready_template()
    database.close()
    repos_db = ReposDatabaseHandler()
    urls, logins, passwords = repos_db.get_backup_repos(master_repo_id)
    repos_db.close()
    backups_list = ""
    for url in urls:
        backups_list.add(url + "\n")

    for email, name in zip(emails, names):
        msg = MIMEMultipart()

        message = message_template.substitute(PERSON_NAME=name, BACKUP_REPOS_LIST=backups_list)

        msg['From'] = email_address
        msg['To'] = email
        msg['Subject'] = "This is test"

        print("send email to " + name + " " + email)
        print(message)



        msg.attach(MIMEText(message, 'plain'))


        # na wszelki wypadek wylaczone
        # server_ssl.send_message(msg)

        del msg


# notify()