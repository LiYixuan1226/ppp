from bibtexparser.bibdatabase import BibDatabase
import datetime
import json

class JsonToBib(object):
    def parse_ieee_json_type(self, ieee_article):  # 解析ieee的json
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
        elif ieee_type == 'Books':
            return 'book'
        else:
            print(ieee_article)

    def parse_ieee_json_authors(self,ieee_article):  # 找作者
        ieee_authors = ieee_article['authors']['authors']
        authors = map(lambda a: a['full_name'], ieee_authors)
        return " and ".join(authors)

    def parse_ieee_json_date(self, ieee_article):  # 找日期

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

    def parse_ieee_abstract(self, ieee_article):  # 解析摘要
        if 'abstract' in ieee_article:
            return ieee_article['abstract']
        elif 'abstract_url' in ieee_article:
            abstract_url = ieee_article['abstract_url']
            return abstract_url

    def parse_extra_bibtex_article_fields(self, ieee_article, new_entry):
        new_entry['journal'] = ieee_article['publication_title']
        if 'issue' in ieee_article:
            new_entry['issue'] = ieee_article['issue']
        if 'volume' in ieee_article:
            new_entry['volume'] = ieee_article['volume']

    def parse_ieee_json_keywords(self, ieee_article):
        article_terms = ieee_article['index_terms']
        entry_terms = list()
        if 'ieee_terms' in article_terms:
            entry_terms += article_terms['ieee_terms']['terms']
        if 'author_terms' in article_terms:
            entry_terms += article_terms['author_terms']['terms']

        return ", ".join(entry_terms)

    def convert_ieee_xplore_json_to_bibtex_db(self, json_string):  # 把json转成bib的格式
        result = BibDatabase()
        #big_list_of_entries = list()
        count = 0
        for ieee_article in json.loads(json_string)['articles']:
            print(ieee_article)
            #big_list_of_entries.append(ieee_article)
            count += 1
            # print(big_list_of_entries[count])
            try:
                new_entry = dict()

                new_entry['ID'] = ieee_article['article_number']
                new_entry['ENTRYTYPE'] = self.parse_ieee_json_type(ieee_article)

                new_entry['abstract'] = self.parse_ieee_abstract(ieee_article)
                new_entry['title'] = ieee_article['title']

                if 'authors' in ieee_article:
                    new_entry['author'] = self.parse_ieee_json_authors(ieee_article)

                new_entry['keywords'] = self.parse_ieee_json_keywords(ieee_article)

                new_entry['url'] = ieee_article['pdf_url']

                if new_entry['ENTRYTYPE'] == 'article':
                    self.parse_extra_bibtex_article_fields(ieee_article, new_entry)

                elif new_entry['ENTRYTYPE'] == 'inproceedings':
                    new_entry['booktitle'] = ieee_article['publication_title']

                article_date = self.parse_ieee_json_date(ieee_article)
                new_entry['year'] = article_date.strftime("%Y")
                new_entry['month'] = article_date.strftime("%B")

                new_entry['pages'] = ("%s-%s") % (ieee_article['start_page'], ieee_article['end_page'])

                result.get_entry_list().append(new_entry)
            except AttributeError:
                continue
            except KeyError:
                continue
        # download(big_list_of_entries, count, path)
        return result,count