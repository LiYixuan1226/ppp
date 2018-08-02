import datetime
import json
import requests

from bibtexparser.bibdatabase import BibDatabase


def parse_ieee_json_type(ieee_article):
    ieee_type = ieee_article['content_type']

    if ieee_type in {'Journals', 'Early Access'}:
        return 'article'
    elif ieee_type == 'Conferences':
        if 'publication_title' in ieee_article:
            return 'inproceedings'
        else:
            return 'proceedings'
    elif ieee_type == 'Standards':
        return 'manual'
    else:
        print(ieee_article)


def parse_ieee_json_authors(ieee_article):
    ieee_authors = ieee_article['authors']['authors']
    authors = map(lambda a: a['full_name'], ieee_authors)
    return " and ".join(authors)


def parse_ieee_json_date(ieee_article):

    if 'publication_date' in ieee_article:
        date_string = ieee_article['publication_date']
    elif 'conference_dates' in ieee_article:
        date_string = ieee_article['conference_dates']
    else:
        return datetime.date.today()

    if '-' in date_string:
        date_string = date_string[date_string.index('-') + 1:]
    if '/' in date_string:
        date_string = date_string[date_string.index('/') + 1:]

    date_string = date_string.replace('Sept.', 'sep.')

    for date_format in ["%b. %d %Y", "%d %b. %Y", "%B %d %Y", "%m %Y", "%Y", "%d %B %Y", "%B %Y"]:
        try:
            return datetime.datetime.strptime(date_string, date_format)
        except ValueError as value_error:
            pass
            # print(value_error)
    print("Warning, couldn't parse date ", date_string)


def parse_ieee_abstract(ieee_article):
    if 'abstract' in ieee_article:
        return ieee_article['abstract']
    elif 'abstract_url' in ieee_article:
        abstract_url = ieee_article['abstract_url']
        return abstract_url


def parse_extra_bibtex_article_fields(ieee_article, new_entry):
    new_entry['journal'] = ieee_article['publication_title']
    if 'issue' in ieee_article:
        new_entry['issue'] = ieee_article['issue']
    if 'volume' in ieee_article:
        new_entry['volume'] = ieee_article['volume']


def parse_ieee_json_keywords(ieee_article):
    article_terms = ieee_article['index_terms']
    entry_terms = list()
    if 'ieee_terms' in article_terms:
        entry_terms += article_terms['ieee_terms']['terms']
    if 'author_terms' in article_terms:
        entry_terms += article_terms['author_terms']['terms']

    return ", ".join(entry_terms)


def convert_ieee_xplore_json_to_bibtex_db(json_string):

    result = BibDatabase()

    for ieee_article in json.loads(json_string)['articles']:
        new_entry = dict()

        new_entry['ID'] = ieee_article['article_number']
        new_entry['ENTRYTYPE'] = parse_ieee_json_type(ieee_article)

        new_entry['abstract'] = parse_ieee_abstract(ieee_article)
        new_entry['title'] = ieee_article['title']

        if 'authors' in ieee_article:
            new_entry['author'] = parse_ieee_json_authors(ieee_article)

        new_entry['keywords'] = parse_ieee_json_keywords(ieee_article)

        new_entry['url'] = ieee_article['pdf_url']

        if new_entry['ENTRYTYPE'] == 'article':
            parse_extra_bibtex_article_fields(ieee_article, new_entry)

        elif new_entry['ENTRYTYPE'] == 'inproceedings':
            new_entry['booktitle'] = ieee_article['publication_title']

        article_date = parse_ieee_json_date(ieee_article)
        new_entry['year'] = article_date.strftime("%Y")
        new_entry['month'] = article_date.strftime("%B")

        new_entry['pages'] = ("%s-%s") % (ieee_article['start_page'], ieee_article['end_page'])

        result.get_entry_list().append(new_entry)

    return result


class IEEEXploreRetrieve(object):

    def __init__(self, queries, api_key):
        self.api_key = api_key
        self.queries = queries

        self.cookies = {}

    def pull(self):
        url_template = 'http://ieeexploreapi.ieee.org/api/v1/search/articles?querytext=%s&apikey=%s'

        user_agents = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64)',
            'AppleWebKit/537.36 (KHTML, like Gecko)',
            'Chrome/35.0.1916.114 Safari/537.36']

        headers = {'User-Agent': " ".join(user_agents)}

        for query in self.queries:
            url = url_template % (query, self.api_key)
            try:
                response = requests.get(url, cookies=self.cookies, headers=headers)
            except ConnectionError:
                # TODO Wrap connection error with a Pipeline Exception.
                return None

        return convert_ieee_xplore_json_to_bibtex_db(response.text)

if __name__ == '__main__':
    query = ''
    api_key = 'xxbuhzj7q5zfednrb9j49yzq'
    ieee_retrieve = IEEEXploreRetrieve([query], api_key)
    bibtex_database = springerlink_retrieve.pull()
    print(bibtex_database)