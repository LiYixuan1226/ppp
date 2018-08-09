import requests
import jsonToBib
import json
from bibtexparser.bibdatabase import BibDatabase


class IEEEXploreRetrieve(object):

    jsonToBib = jsonToBib.JsonToBib()

    def __init__(self, queries, api_key, maximum_results=-1):
        self.api_key = api_key
        self.queries = queries
        self.maximum_results = maximum_results
        self.cookies = {}

    def pull(self):

        result = BibDatabase()

        for query in self.queries:

            start = 1
            while len(result.entries) < self.maximum_results or self.maximum_results == -1:

                # gets about 200 results from ieee
                response = self.retrieve_page_of_results(query, start)

                # converts the 200 json entries to bibtex entries
                new_database, count = self.jsonToBib.convert_ieee_xplore_json_to_bibtex_db(response.text)
                new_entries = new_database.entries

                # adds 200 entries to result database
                result.entries.extend(new_entries)
                print(len(result.entries), self.maximum_results)

            if eval(response.text)['total_records']=="0":
                break

            start += 200

        big_list_of_entries = list()
        for ieee_article in json.loads(response.text)['articles']:
            big_list_of_entries.append(ieee_article)

        big_list_of_entries = big_list_of_entries[0:self.maximum_results]

        return result, big_list_of_entries, count

    def retrieve_page_of_results(self, query, start):
        url_template = 'http://ieeexploreapi.ieee.org/api/v1/search/articles?querytext=%s&apikey=%s&start_record=%d&max_records=200'

        user_agents = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64)',
            'AppleWebKit/537.36 (KHTML, like Gecko)',
            'Chrome/35.0.1916.114 Safari/537.36']

        headers = {'User-Agent': " ".join(user_agents)}

        url = url_template % (query, self.api_key, start)
        try:
            return requests.get(url, cookies=self.cookies, headers=headers)
        except ConnectionError:
            # TODO Wrap connection error with a Pipeline Exception.
            return None

