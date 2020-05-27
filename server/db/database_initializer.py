from database_handler import ReposDatabaseHandler, EmailsDatabaseHandler

repos_db = ReposDatabaseHandler()
repos_db.create_master_repos_and_backup_repos_tables()
repos_db.close()
emails_db = EmailsDatabaseHandler()
emails_db.create_email_tables()
emails_db.close()