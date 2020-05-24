import json
import requests

class Scrapper:
    def __init__(self, repo_url):
        self.repo_url = repo_url

    def scrap_associated(self):
        # docelowo możemy pobierać już gotowy słownik i tylko do aktualizować
        emails = dict()

        github_url = True
        if not github_url:
            return
        prefix = "https://github.com/"

        def _remove_prefix(text, prefix):
            return text[text.startswith(prefix) and len(prefix):]
        user_and_repo_name = _remove_prefix(self.repo_url, prefix)

        stargazers = requests.get("https://api.github.com/repos/" + user_and_repo_name + "/stargazers").json()
        #TODO limity dodac obsluge wyjatkow
        for s in stargazers:
            login = s.get('login')
            if emails.get(login, None) != None:
                continue
            url = "https://api.github.com/users/" + login +"/events/public"
            user_stat = requests.get(url).json()
            for event in user_stat:
                if event.get('type') == 'PushEvent':
                    commits = event.get('payload').get('commits')
                    email = commits[0].get('author').get('email')
                    emails.update({login: email})
                    break

        contributors = requests.get("https://api.github.com/repos/" + user_and_repo_name + "/contributors").json()
        for c in contributors:
            login = c.get('login')
            if emails.get(login, None) != None:
                continue
            url = "https://api.github.com/users/" + login +"/events/public"
            user_stat = requests.get(url).json()
            for event in user_stat:
                if event.get('type') == 'PushEvent':
                    commits = event.get('payload').get('commits')
                    email = commits[0].get('author').get('email')
                    emails.update({login: email})
                    break

        print(emails)
        return emails

