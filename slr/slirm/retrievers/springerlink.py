import datetime
import json
import requests
from bibtexparser.bibdatabase import BibDatabase



class SpringerLinkRetrieve(object):

    def __init__(self, queries, api_key):
        self.api_key = api_key
        self.queries = queries

        self.cookies = {}

    def pull(self):
        url_template = 'http://api.springernature.com/metadata/pam/doi/10.1007/s11276-008-0131-4?api_key='

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
        print("response:" + response.text)
        return response.text

if __name__ == '__main__':
    query = 'software testing'
    api_key = 'a6cb064309bb238a35a383a30f510748'
    springerlink_retrieve = SpringerLinkRetrieve([query], api_key)
    bibtex_database = springerlink_retrieve.pull()
    print("bibtex:"+bibtex_database)
