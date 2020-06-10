from os.path import expanduser
import os


class DBLocation:
    def __init__(self):
        if expanduser("~") == "C:\\Users\\Lenovo":
            self.home_sql_lite = expanduser("~") + "\\kbieniasz_tmp\\projects\\Git-sync\\gitSync.database_maintenance"
        elif expanduser("~") == "C:\\Users\\kbien":
            self.home_sql_lite = expanduser("~") + "\\PycharmProjects\\Git-sync\\gitSync.database_maintenance"
        else:
            self.home_sql_lite = os.path.join(expanduser("~"), "gitSync.database_maintenance")



location = DBLocation()
print(location.home_sql_lite)
# if expanduser("~") == "C:\\Users\\Lenovo":
#     print("ok")
