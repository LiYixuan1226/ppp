import requests

from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode


class ACMRetrieve(object):

    def __init__(self, queries):
        self.cookies = {}
        self.queries = queries

    def pull(self):
        user_agents = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64)',
            'AppleWebKit/537.36 (KHTML, like Gecko)',
            'Chrome/35.0.1916.114 Safari/537.36']

        headers = {'User-Agent': " ".join(user_agents)}
        within = 'owners%%2Eowner%%3DHOSTED'
        sort = '%%5Fscore'
        export_format = 'bibtex'
        url_template = 'https://dl.acm.org/exportformats_search.cfm?query=%s&within=%s&srt=%s&expformat=%s'

        result = BibDatabase()

        for query in self.queries:
            url = url_template % (query, within, sort, export_format)
            response = requests.get(url, cookies=self.cookies, headers=headers)
            self.cookies.update(response.cookies)
            bibtex_parser = BibTexParser(customization=convert_to_unicode)

            result.get_entry_list().append(bibtex_parser.parse(response.text).get_entry_list())

        return result
