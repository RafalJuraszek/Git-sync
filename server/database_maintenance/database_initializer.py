from notificator.email_client.notificator import ReposDatabaseHandler, EmailsDatabaseHandler

class DatabaseInitializer:
    def create_tables_if_not_exist(self):
        repos_db = ReposDatabaseHandler()
        repos_db.create_master_repos_and_backup_repos_tables()
        repos_db.close()
        emails_db = EmailsDatabaseHandler()
        emails_db.create_email_tables()
        emails_db.close()