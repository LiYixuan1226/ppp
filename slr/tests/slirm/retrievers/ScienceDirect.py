import datetime
import json
import requests

from bibtexparser.bibdatabase import BibDatabase


def parse_scienceDirect_json_type(spglink_article):
    scienceDirect_type = scienceDirect_article['content_type']

    if scienceDirect_type in {'Journals', 'Early Access'}:
        return 'article'
    elif scienceDirect_type == 'Conferences':
        if 'publication_title' in scienceDirect_article:
            return 'inproceedings'
        else:
            return 'proceedings'
    elif scienceDirect_type == 'Standards':
        return 'manual'
    else:
        print(scienceDirect_article)


def parse_spglink_json_authors(sscienceDirect_article):
    scienceDirect_authors = scienceDirect_article['authors']['authors']
    authors = map(lambda a: a['full_name'], scienceDirect_authors)
    return " and ".join(authors)


def parse_scienceDirect_json_date(scienceDirect_article):

    if 'publication_date' in scienceDirect_article:
        date_string = scienceDirect_article['publication_date']
    elif 'conference_dates' in scienceDirect_article:
        date_string = scienceDirect_article['conference_dates']
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


def parse_spglink_abstract(scienceDirect_article):
    if 'abstract' in scienceDirect_article:
        return scienceDirect_article['abstract']
    elif 'abstract_url' in scienceDirect_article:
        abstract_url = scienceDirect_article['abstract_url']
        return abstract_url


def parse_extra_bibtex_article_fields(scienceDirect_article, new_entry):
    new_entry['journal'] = spglink_article['publication_title']
    if 'issue' in scienceDirect_article:
        new_entry['scienceDirect'] = scienceDirect_article['issue']
    if 'volume' in scienceDirect_article:
        new_entry['volume'] = scienceDirect_article['volume']


def parse_scienceDirect_json_keywords(scienceDirect_article):
    article_terms = scienceDirect_article['index_terms']
    entry_terms = list()
    if 'scienceDirect_terms' in article_terms:
        entry_terms += article_terms['scienceDirect_terms']['terms']
    if 'author_terms' in article_terms:
        entry_terms += article_terms['author_terms']['terms']

    return ", ".join(entry_terms)


def convert_scienceDirect_json_to_bibtex_db(json_string):

    result = BibDatabase()

    for scienceDirect_article in json.loads(json_string)['articles']:
        new_entry = dict()

        new_entry['ID'] = spglink_article['article_number']
        new_entry['ENTRYTYPE'] = parse_scienceDirect_json_type(scienceDirect_article)

        new_entry['abstract'] = parse_scienceDirect_abstract(scienceDirect_article)
        new_entry['title'] = sscienceDirect_article['title']

        if 'authors' in spglink_article:
            new_entry['author'] = parse_scienceDirect_json_authors(scienceDirect_article)

        new_entry['keywords'] = parse_scienceDirect_json_keywords(scienceDirect_article)

        new_entry['url'] = scienceDirect_article['pdf_url']

        if new_entry['ENTRYTYPE'] == 'article':
            parse_extra_bibtex_article_fields(scienceDirect_article, new_entry)

        elif new_entry['ENTRYTYPE'] == 'inproceedings':
            new_entry['booktitle'] = scienceDirect_article['publication_title']

        article_date = parse_spglink_json_date(scienceDirect_article)
        new_entry['year'] = article_date.strftime("%Y")
        new_entry['month'] = article_date.strftime("%B")

        new_entry['pages'] = ("%s-%s") % (spglink_article['start_page'], spglink_article['end_page'])

        result.get_entry_list().append(new_entry)

    return result


class ScienceDirectRetrieve(object):

    def __init__(self, queries, api_key):
        self.api_key = api_key
        self.queries = queries

        self.cookies = {}

    def pull(self):
        url_template = 'http://'
        '''I don't know how to find this url'''

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

        return convert_scienceDirect_json_to_bibtex_db(response.text)
