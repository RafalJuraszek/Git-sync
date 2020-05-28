from os.path import expanduser
import os


class DBLocation:
    def __init__(self):
        #self.home_sql_lite = expanduser("~") + "\\kbieniasz_tmp\\projects\\Git-sync\\gitSync.db"
        self.home_sql_lite = expanduser("~") + "\\gitSync.db"


location = DBLocation()
print(location.home_sql_lite)