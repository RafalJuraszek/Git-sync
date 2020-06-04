class MockDb:
    def __init__(self):
        pass
#logins, passwords, paths, periods
    def get_master_repos(self):
        return (['test', 'test2'],
                ['https://github.com/Roshoy/test', 'https://github.com/Roshoy/test2'],
                ['Roshoy', 'Roshoy'],
                ['dummy', 'dummy'],
                [r'C:\Users\Adrian\Studia\IoTest', r'C:\Users\Adrian\Studia\IoTest2'],
                [30, 35])

    def get_backup_repos(self, master_repo_id):
        if master_repo_id == 'test':
            return (['https://bitbucket.org/IoTeamRak/test.git'],
                    ['IoTeamRak'],
                    ['Q1w2e3r4'])
        return (['https://bitbucket.org/IoTeamRak/test22.git'],
                ['IoTeamRak'],
                ['Q1w2e3r4'])