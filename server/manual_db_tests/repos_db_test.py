from server.db.database_handler import ReposDatabaseHandler
print('test')
repos_db = ReposDatabaseHandler()
sql_create_master_repos_table = """ CREATE TABLE IF NOT EXISTS master_repos (
                                                id text PRIMARY KEY,
                                                url text NOT NULL,
                                                login text NOT NULL,
                                                password text NOT NULL,
                                                path NOT NULL UNIQUE,
                                                frequency integer NOT NULL
                                            ); """
repos_db
repos_db.insert_data_master_repos('git-syncccc', 'kbieniasz', 'wwwww', 'haslo', 'sciezkaakaa',4)
repos_db.close()
