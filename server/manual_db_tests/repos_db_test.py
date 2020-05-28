from server.db.database_handler import ReposDatabaseHandler

repos_db = ReposDatabaseHandler()
repos_db.insert_data_master_repos('ids', 'logins', 'urls', 'pass', 'paths',2)
repos_db.close()