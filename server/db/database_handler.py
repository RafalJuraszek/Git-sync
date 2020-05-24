import sqlite3


class EmailsDatabaseHandler:

    def __init__(self) -> None:
        try:
            self.connection = sqlite3.connect('database.db')
            self.cursor = self.connection.cursor()
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)

    def create_email_table(self):
        try:
            table_query = 'CREATE TABLE IF NOT EXISTS emails (email TEXT PRIMARY KEY,name TEXT NOT NULL)'
            self.cursor.execute(table_query)
            self.connection.commit()
            print("SQLite table created")
        except sqlite3.Error as error:
            print("Error while creating table ", error)
    def get_data(self):
        try:
            select_query = """SELECT * from emails"""
            self.cursor.execute(select_query)
            records = self.cursor.fetchall()
            names = []
            emails = []
            for row in records:
                emails.append(row[0])
                names.append(row[1])
            return emails, names
        except sqlite3.Error as error:
            print("Error while selecting from table ")
    def insert_data(self, email, name):
        try:
            insert_query = """INSERT INTO emails
                          (email, name) 
                           VALUES 
                          (?, ?)"""
            data_tuple = (email, name)
            self.cursor.execute(insert_query, data_tuple)
            self.connection.commit()
        except sqlite3.Error as error:
            print("Error while inserting to table ")
    def close(self):
        self.cursor.close()
        self.connection.close()
