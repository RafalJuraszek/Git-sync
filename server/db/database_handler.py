import sqlite3


class EmailsDatabaseHandler:

    def __init__(self) -> None:
        try:
            self.connection = sqlite3.connect('database.db')
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
                                                                FOREIGN KEY (master_repo_id) REFERENCES master_repos (id) ON DELETE CASCADE,
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
                        inner join master_repos as mr on er.master_repo_id = mr.id"""
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
                        inner join master_repos as mr on er.master_repo_id = mr.id
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


    def insert_data(self, email, name, master_repo_id):
        try:
            insert_query = """INSERT INTO emails
                          (name, email) 
                           VALUES 
                          (?,?)"""
            data_tuple = (name, email)
            self.cursor.execute(insert_query, data_tuple)
            self.connection.commit()
            insert_query = """INSERT INTO emails_repos
                          (name, master_repo_id) 
                           VALUES 
                          (?,?)"""
            data_tuple = (name, master_repo_id)
            self.cursor.execute(insert_query, data_tuple)
            self.connection.commit()
        except sqlite3.Error as error:
            print("Error while inserting to table ")
    def close(self):
        self.cursor.close()
        self.connection.close()


class ReposDatabaseHandler:
    def __init__(self) -> None:
        try:
            self.connection = sqlite3.connect('database.db')
            self.cursor = self.connection.cursor()
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)

    def create_master_repos_and_backup_repos_tables(self):
        try:
            sql_create_master_repos_table = """ CREATE TABLE IF NOT EXISTS master_repos (
                                                id text PRIMARY KEY,
                                                url text NOT NULL,
                                                login text NOT NULL,
                                                password text NOT NULL,
                                                path NOT NULL UNIQUE,
                                                frequency integer NOT NULL
                                            ); """

            sql_create_backup_repos_table = """CREATE TABLE IF NOT EXISTS backup_repos (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            master_repo_id text NOT NULL,
                                            url text NOT NULL,
                                            login text NOT NULL,
                                            password text NOT NULL,
                                            FOREIGN KEY (master_repo_id) REFERENCES master_repos (id) ON DELETE CASCADE,
                                            UNIQUE(master_repo_id, url)
                                        );"""

            self.cursor.execute(sql_create_master_repos_table)
            self.connection.commit()
            self.cursor.execute(sql_create_backup_repos_table)
            self.connection.commit()
            print("SQLite table created")
        except sqlite3.Error as error:
            print("Error while creating table ", error)



    def insert_data_master_repos(self, id, url, login, password, path, frequency):
        try:
            insert_query = """INSERT INTO master_repos
                          (id, url, login, password, path, frequency) 
                           VALUES 
                          (?, ?, ?, ?, ?, ?)"""
            data_tuple = (id, url, login, password, path, frequency)
            self.cursor.execute(insert_query, data_tuple)
            self.connection.commit()
        except sqlite3.Error as error:
            print("Error while inserting to table master_repos")


    def insert_data_backup_repos(self, master_repo_id, url, login, password):
        try:
            insert_query = """INSERT INTO backup_repos
                          (master_repo_id, url, login, password) 
                           VALUES 
                          (?, ?, ?, ?)"""
            data_tuple = ( master_repo_id, url, login, password)
            self.cursor.execute(insert_query, data_tuple)
            self.connection.commit()
        except sqlite3.Error as error:
            print("Error while inserting to table backup_repos")

    def update_frequency_master_repos(self, id, frequency):
        try:
            update_query = """UPDATE master_repos
                            SET frequency = ?
                            WHERE id = ?"""
            data_tuple = ( frequency, id)
            self.cursor.execute(update_query, data_tuple)
            self.connection.commit()
        except sqlite3.Error as error:
            print("Error while inserting to table backup_repos")

    def update_backup_repo(self, master_repo_id,url, login, password):
        try:
            update_query = """UPDATE backup_repos
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
            select_query = """SELECT * from  backup_repos
                            WHERE master_repo_id = ? AND  url = ?"""
            data_tuple = ( master_repo_id, url)
            self.cursor.execute(select_query, data_tuple)
            if len(self.cursor.fetchall()) == 0:
                self.insert_data_backup_repos(master_repo_id,url, login, password)
            else:
                self.update_backup_repo(master_repo_id,url, login, password)
        except sqlite3.Error as error:
            print("Error while select * from table backup_repos")

    def get_master_repos(self):
        try:
            select_query = """SELECT id, url, login, password, path, frequency from master_repos"""
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
            return ids, urls, logins, passwords, paths, frequency
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
                urls.append(row[0])
                logins.append(row[1])
                passwords.append(row[2])
            return urls, logins, passwords
        except sqlite3.Error as error:
            print("Error while selecting from table backup_repos")


    def delete_master_repo(self, master_repo_id):
        try:
            delete_query = """DELETE FROM master_repos WHERE id = ?"""
            self.cursor.execute(delete_query,(master_repo_id, ))
        except sqlite3.Error as error:
            print("Error while deleting from table master_repos")

    def delete_backup_repo(self, master_repo_id, url):
        try:
            delete_query = """DELETE FROM backup_repos WHERE master_repo_id = ? AND url = ?"""
            self.cursor.execute(delete_query,(master_repo_id, url))
        except sqlite3.Error as error:
            print("Error while deleting from table backup_repos")



    def close(self):
        self.cursor.close()
        self.connection.close()