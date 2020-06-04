import sqlite3
from server.db.database_localizator import DBLocation
from server.db.error_messages_for_user import *

class EmailsDatabaseHandler:

    def __init__(self) -> None:
        try:
            self.connection = sqlite3.connect(DBLocation().home_sql_lite)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)

    def create_email_tables(self):
        try:
            table_query = """CREATE TABLE IF NOT EXISTS emails (name TEXT PRIMARY KEY,
                                                                email TEXT NOT NULL
                                                                )"""
            self.cursor.execute(table_query)
            self.connection.commit()
            table_query = """CREATE TABLE IF NOT EXISTS emails_repos (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                name TEXT NOT NULL,
                                                                master_repo_id TEXT NOT NULL,
                                                                FOREIGN KEY (master_repo_id) REFERENCES masterRepos (id) ON DELETE CASCADE,
                                                                FOREIGN KEY (name) REFERENCES emails (name) ON DELETE CASCADE
                                                                )"""
            self.cursor.execute(table_query)
            self.connection.commit()
            print("SQLite tables emails, emails_repos created")
        except sqlite3.Error as error:
            print("Error while creating table ", error)
    def get_data(self):
        try:
            select_query = """SELECT e.email, e.name, mr.id
                        from emails as e 
                        inner join emails_repos as er on e.name = er.name
                        inner join masterRepos as mr on er.master_repo_id = mr.id"""
            self.cursor.execute(select_query)
            records = self.cursor.fetchall()
            names = []
            emails = []
            repos = []
            for row in records:
                emails.append(row[0])
                names.append(row[1])
                repos.append(row[2])
            return emails, names, repos
        except sqlite3.Error as error:
            print("Error while selecting from table ")

    def get_data_where_master_repo(self, master_repo_id):
        try:
            select_query = """SELECT e.email, e.name
                        from emails as e 
                        inner join emails_repos as er on e.name = er.name
                        inner join masterRepos as mr on er.master_repo_id = mr.id
                        WHERE mr.id = ?"""
            self.cursor.execute(select_query, (master_repo_id, ))
            records = self.cursor.fetchall()
            names = []
            emails = []
            for row in records:
                emails.append(row[0])
                names.append(row[1])
            return emails, names
        except sqlite3.Error as error:
            print("Error while selecting from table ")


    def insert_data_to_email(self, name, email):
        try:
            sqliteConnection = sqlite3.connect(DBLocation().home_sql_lite)
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")
            select =  """SELECT  *
                        FROM    emails 
                        WHERE   name = ?"""

            self.cursor.execute(select, (name, ))
            records = self.cursor.fetchall()
            if len(records) == 0:
                sqlite_insert_with_param = """
                            INSERT INTO emails
                                  (name, email) 
                                   VALUES 
                                  (?, ?)
                        """

                data_tuple = (name, email)
                cursor.execute(sqlite_insert_with_param, data_tuple)
                sqliteConnection.commit()
                print("Insert or not to emails")
        except sqlite3.Error as error:
            print("Error while inserting to emails", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("sqlite connection is closed")



    def insert_data_to_email_repos(self, name, master_repo_id):
        try:
            sqliteConnection = sqlite3.connect(DBLocation().home_sql_lite)
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            select = """SELECT  *
                        FROM    emails_repos 
                        WHERE   name = ? AND master_repo_id = ?"""
            self.cursor.execute(select, (name, master_repo_id ))
            records = self.cursor.fetchall()
            if len(records) == 0:
                sqlite_insert_with_param = """
                            INSERT INTO emails_repos
                                  (name, master_repo_id) 
                                   VALUES 
                                  (?, ?)
                        """

                data_tuple = (name, master_repo_id)
                cursor.execute(sqlite_insert_with_param, data_tuple)
                sqliteConnection.commit()
                print("Insert or not to emails")
        except sqlite3.Error as error:
            print("Error while creating a sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("sqlite connection is closed")
    #  zle
    # def insert_data(self, email, name, master_repo_id):
    #     try:
    #         insert_query = """INSERT INTO emails
    #                       (name, email)
    #                        VALUES
    #                       (?,?)"""
    #         data_tuple = (name, email)
    #         self.cursor.execute(insert_query, data_tuple)
    #         self.connection.commit()
    #         insert_query = """INSERT INTO emails_repos
    #                       (name, master_repo_id)
    #                        VALUES
    #                       (?,?)"""
    #         data_tuple = (name, master_repo_id)
    #         self.cursor.execute(insert_query, data_tuple)
    #         self.connection.commit()
    #     except sqlite3.Error as error:
    #         print("Error while inserting to table ")
    def close(self):
        self.cursor.close()
        self.connection.close()


class ReposDatabaseHandler:
    def __init__(self) -> None:
        try:
            self.connection = sqlite3.connect(DBLocation().home_sql_lite)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)

    def create_master_repos_and_backup_repos_tables(self):
        try:
            try:
                sqliteConnection = sqlite3.connect(DBLocation().home_sql_lite)
                sqlite_create_table_query = ''' CREATE TABLE IF NOT EXISTS masterRepos (
                                                            id text PRIMARY KEY,
                                                            url text NOT NULL,
                                                            login text NOT NULL,
                                                            password text NOT NULL,
                                                            path NOT NULL UNIQUE,
                                                            frequency integer NOT NULL
                                                        ); '''

                cursor = sqliteConnection.cursor()
                print("Successfully Connected to SQLite")
                cursor.execute(sqlite_create_table_query)
                sqliteConnection.commit()
                print("SQLite table created")

                cursor.close()

            except sqlite3.Error as error:
                print("Error while creating a sqlite table", error)
            finally:
                if (sqliteConnection):
                    sqliteConnection.close()
                    print("sqlite connection is closed")


            try:
                sqliteConnection = sqlite3.connect(DBLocation().home_sql_lite)
                sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS backupRepos (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            master_repo_id text NOT NULL,
                                            url text NOT NULL,
                                            login text NOT NULL,
                                            password text NOT NULL,
                                            FOREIGN KEY (master_repo_id) REFERENCES masterRepos (id) ON DELETE CASCADE,
                                            UNIQUE(master_repo_id, url)
                                        );'''

                cursor = sqliteConnection.cursor()
                print("Successfully Connected to SQLite")
                cursor.execute(sqlite_create_table_query)
                sqliteConnection.commit()
                print("SQLite table created")

                cursor.close()

            except sqlite3.Error as error:
                print("Error while creating a sqlite table", error)
            finally:
                if (sqliteConnection):
                    sqliteConnection.close()
                    print("sqlite connection is closed")




            # sql_create_master_repos_table = """ CREATE TABLE IF NOT EXISTS master_repos (
            #                                     id text PRIMARY KEY,
            #                                     url text NOT NULL,
            #                                     login text NOT NULL,
            #                                     password text NOT NULL,
            #                                     path NOT NULL UNIQUE,
            #                                     frequency integer NOT NULL
            #                                 ); """
            #
            #
            #
            # self.cursor.execute(sql_create_master_repos_table)
            # self.connection.commit()


            #
            # sql_create_backup_repos_table = """CREATE TABLE IF NOT EXISTS backup_repos (
            #                                 id INTEGER PRIMARY KEY AUTOINCREMENT,
            #                                 master_repo_id text NOT NULL,
            #                                 url text NOT NULL,
            #                                 login text NOT NULL,
            #                                 password text NOT NULL,
            #                                 FOREIGN KEY (master_repo_id) REFERENCES master_repos (id) ON DELETE CASCADE,
            #                                 UNIQUE(master_repo_id, url)
            #                             );"""
            # self.cursor.execute(sql_create_backup_repos_table)
            # self.connection.commit()
            # print("SQLite table created")
        except sqlite3.Error as error:
            print("Error while creating table ", error)



    def insert_data_master_repos(self, id, url, login, password, path, frequency):
        return_message = "ok"
        try:
            sqliteConnection = sqlite3.connect(DBLocation().home_sql_lite)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")

            sqlite_insert_with_param = """INSERT INTO masterRepos
                              (id, url, login, password, path, frequency) 
                               VALUES 
                              (?, ?, ?, ?, ?, ?)"""

            data_tuple = (id, url, login, password, path, frequency)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqliteConnection.commit()
            print("DB inserted successfully into master_repos table")
        except sqlite3.Error as error:
            print("Error while creating a sqlite table", error)
            return_message = master_repo_insert_error
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                # print("sqlite connection is closed")
                # print(">>>>>>>>>>" + return_message)
                return return_message




    def insert_data_backup_repos(self, master_repo_id, url, login, password):
        return_message = "ok"
        try:
            # print(">>>>>>>>>>>>>>>>>> Dodawanie backupu")
            sqliteConnection = sqlite3.connect(DBLocation().home_sql_lite)
            cursor = sqliteConnection.cursor()
            # print("Connected to SQLite")

            sqlite_insert_with_param = """INSERT INTO backupRepos
                              (master_repo_id, url, login, password)  
                               VALUES 
                              (?, ?, ?, ?)"""

            data_tuple = (master_repo_id, url, login, password)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqliteConnection.commit()
            print("Python Variables inserted successfully into backup_repos table")
        except sqlite3.Error as error:
            print("Error while creating a sqlite table", error)
            return_message = reapeted_combinatio_master_backup_url(master_repo_id, url)

        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                # print("sqlite connection is closed")
                return return_message


    def update_frequency_master_repos(self, id, frequency):
        try:
            update_query = """UPDATE masterRepos
                            SET frequency = ?
                            WHERE id = ?"""
            data_tuple = ( frequency, id)
            self.cursor.execute(update_query, data_tuple)
            self.connection.commit()
        except sqlite3.Error as error:
            print("Error while updating frequency in table masterRepos")

    def update_backup_repo(self, master_repo_id,url, login, password):
        try:
            update_query = """UPDATE backupRepos
                            SET login = ?,
                                password = ? 
                            WHERE master_repo_id = ? AND url = ?"""
            data_tuple = ( login,password, master_repo_id, url)
            self.cursor.execute(update_query, data_tuple)
            self.connection.commit()
        except sqlite3.Error as error:
            print("Error while updating table backup_repos")

    def update_or_create_backup_repo(self, master_repo_id,url, login, password):
        try:
            select_query = """SELECT * from  backupRepos
                            WHERE master_repo_id = ? AND  url = ?"""
            data_tuple = ( master_repo_id, url)
            self.cursor.execute(select_query, data_tuple)
            if len(self.cursor.fetchall()) == 0:
                self.insert_data_backup_repos(master_repo_id,url, login, password)
            else:
                self.update_backup_repo(master_repo_id,url, login, password)
        except sqlite3.Error as error:
            print("Error while select * from table backup_repos")
            print(error)

    def get_master_repos(self):
        try:
            select_query = """SELECT id, url, login, password, path, frequency from masterRepos"""
            self.cursor.execute(select_query)
            records = self.cursor.fetchall()
            ids = []
            urls = []
            logins = []
            passwords = []
            paths = []
            frequency = []
            for row in records:
                ids.append(row[0])
                urls.append(row[1])
                logins.append(row[2])
                passwords.append(row[3])
                paths.append(row[4])
                frequency.append(row[5])
            print("get debug")
            print(ids)
            return [ids, urls, logins, passwords, paths, frequency]
        except sqlite3.Error as error:
            print("Error while selecting from table master_repos")




    def get_master_repo_url(self, id):
        try:
            select_query = """SELECT url from masterRepos where id = ?"""
            self.cursor.execute(select_query,(id, ))
            records = self.cursor.fetchall()
            print("records" + str(records))
            urls = []

            for row in records:
                urls.append(row[0])
            url = urls[0]
            return url
        except sqlite3.Error as error:
            print("Error while selecting from table master_repos")

    def get_backup_repos(self, master_repo_id):
        try:
            select_query = """SELECT url, login, password from backup_repos WHERE master_repo_id = ?"""
            self.cursor.execute(select_query,(master_repo_id, ))
            records = self.cursor.fetchall()
            urls = []
            logins = []
            passwords = []
            for row in records:
                print("jakies backupy")
                urls.append(row[0])
                logins.append(row[1])
                passwords.append(row[2])
            return urls, logins, passwords
        except sqlite3.Error as error:
            print("Error while selecting from table backup_repos")


    def delete_master_repo(self, master_repo_id):
        try:
            delete_query = """DELETE FROM masterRepos WHERE id = ?"""
            print("delete master debug")
            print(delete_query)
            self.cursor.execute(delete_query,(master_repo_id, ))
            self.connection.commit()
        except sqlite3.Error as error:
            print("Error while deleting from table master_repos")
            print(error)

    def delete_backup_repo(self, master_repo_id, url):
        try:
            delete_query = """DELETE FROM backupRepos WHERE master_repo_id = ? AND url = ?"""
            self.cursor.execute(delete_query,(master_repo_id, url))
            self.connection.commit()
        except sqlite3.Error as error:
            print("Error while deleting from table backup_repos")
            print(error)



    def close(self):
        self.cursor.close()
        self.connection.close()