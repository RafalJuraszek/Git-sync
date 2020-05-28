from server.db.database_handler import ReposDatabaseHandler
print('test')
repos_db = ReposDatabaseHandler()
# repos_db.create_master_repos_and_backup_repos_tables()
repos_db.insert_data_master_repos('git-synccscc', 'kbiesniasz', 'wwswww', 'hasslo', 'sciezksaakaa',4)
repos_db.close()
