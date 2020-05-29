from server.scrapper.scrapper import Scrapper
repo_url = "https://github.com/mnabywan/Ontology"

s = Scrapper(repo_url=repo_url)
s.scrap_associated()