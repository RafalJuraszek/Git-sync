import sqlite3

try:
    sqliteConnection = sqlite3.connect('backup.database_maintenance')
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



# try:
#     sqliteConnection = sqlite3.connect('SQLite_Python.database_maintenance')
#     cursor = sqliteConnection.cursor()
#     print("Successfully Connected to SQLite")
#
#     sqlite_insert_query = """INSERT INTO SqliteDb_developers
#                           (id, name, email, joining_date, salary)
#                            VALUES
#                           (1,'James','james@pynative.com','2019-03-17',8000)"""
#
#     count = cursor.execute(sqlite_insert_query)
#     sqliteConnection.commit()
#     print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
#     cursor.close()
#
# except sqlite3.Error as error:
#     print("Failed to insert data into sqlite table", error)
# finally:
#     if (sqliteConnection):
#         sqliteConnection.close()
#         print("The SQLite connection is closed")


def insertVaribleIntoTable(id, url, login, password, path, frequency):
    try:
        sqliteConnection = sqlite3.connect('backup.database_maintenance')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param =  """INSERT INTO masterRepos
                          (id, url, login, password, path, frequency) 
                           VALUES 
                          (?, ?, ?, ?, ?, ?)"""

        data_tuple = (id, url, login, password, path, frequency)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into SqliteDb_developers table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

# insertVaribleIntoTable(2, 'Joe', 'joe@pynative.com', '2019-05-19', 9000)
insertVaribleIntoTable('kbieniasz', 'Bene', 'ben@pynative3.com', 'ddssd','dsdsd', 9500)
