import datetime
import json
import requests

from bibtexparser.bibdatabase import BibDatabase


class ScienceDirectRetrieve(object):

    def __init__(self, queries, api_key):
        self.api_key = api_key
        self.queries = queries

        self.cookies = {}

    def pull(self):
        url_template =' http://api.elsevier.com/content/search/scopus?query=heart&apiKey='
        '''I don't know how to find this url'''

        user_agents = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64)',
            'AppleWebKit/537.36 (KHTML, like Gecko)',
            'Chrome/35.0.1916.114 Safari/537.36']

        headers = {'User-Agent': " ".join(user_agents)}

        for query in self.queries:
            url = url_template + self.api_key
            try:
                response = requests.get(url, cookies=self.cookies, headers=headers)
            except ConnectionError:
                # TODO Wrap connection error with a Pipeline Exception.
                return None

        return response.text

if __name__ == '__main__':
    query = 'software testing'
    api_key = '5b8627370566798169844f272c6af106'
    sd_retrieve = ScienceDirectRetrieve([query], api_key)
    bibtex_database = sd_retrieve.pull()
    print(bibtex_database)
