from functools import reduce
from bibtexparser.bibdatabase import BibDatabase
from datetime import date, datetime
import string
import logging


class OneToOneFilter(object):

    def __init__(self, source_pipe, accept=lambda entry: True):
        self.source_pipe = source_pipe
        self.accept = accept

        self.matching_results = None
        self.non_matching_results = None

    def no_match_pipe(self):
        return OneToOneFilter(self.source_pipe, lambda entry: not self.accept(entry))

    def pull(self):
        result = BibDatabase()
        database = self.source_pipe.pull()

        for entry in database.get_entry_list():
            if self.accept(entry):
                result.get_entry_list().append(entry)
        return result


class DateRangeFilter(OneToOneFilter):

    def __init__(self, source_pipe, from_date:date, to_date:date):
        def date_within(entry):
            if 'year' not in entry:
                return False

            year_str = entry['year']
            if "-" in year_str:
                year_str = year_str.split('-')[0]

            if "–" in year_str:
                year_str = year_str.split("–")[0]

            try:
                year = datetime.strptime(year_str, "%Y").date().year
            except ValueError as value_error:
                logging.warning("Couldn't format year string %s,", value_error)
                return False

            month_str = entry.get('month', 'Jan')
            if '-' in month_str:
                month_str = month_str.split('-')[0]
            if '–' in month_str:
                month_str = month_str.split('–')[0]

            if month_str == "Sept":
                month_str = "Sep"

            if len(month_str) < 3:
                month_code = "%m"
            elif len(month_str) == 3:
                month_code = "%b"
            else:
                month_code = "%B"

            try:
                month = datetime.strptime(month_str, month_code).month
                publication_date = date(year, month, 1)
            except ValueError as value_error:
                logging.warning("Couldn't format month string [%s].", value_error)
                publication_date = date(year, 1, 1)

            return from_date <= publication_date <= to_date

        super().__init__(source_pipe, date_within)


class ExcludeKeysFilter(OneToOneFilter):

    def __init__(self, source_pipe, excluded_keys):
        super().__init__(source_pipe, lambda entry: entry['ID'] not in excluded_keys)


class IncludeKeysFilter(OneToOneFilter):
    def __init__(self, source_pipe, included_keys):
        super().__init__(source_pipe, lambda entry: entry['ID'] in included_keys)


class DuplicateEntryFilter(object):

    def __init__(self, source_pipe, key=lambda entry: entry['ID']):
        self.source_pipe = source_pipe
        self.key = key

    def pull(self):
        already_seen = set()

        result = BibDatabase()
        database = self.source_pipe.pull()

        for entry in database.get_entry_list():
            if self.key(entry) not in already_seen:
                already_seen.add(self.key(entry))
                result.get_entry_list().append(entry)

        return result



def make_exclude_terms_match_condition(field_keys, terms):
    def exclude_terms_match_condition(entry):
        for term in terms:
            term = term.lower()
            for field_key in field_keys:
                if term in entry.get(field_key, "").lower():
                    return True
        return False

    return exclude_terms_match_condition


class ExcludeTermFilter(OneToOneFilter):

    def __init__(self, source_pipe, field_keys, terms):
        super().__init__(source_pipe, make_exclude_terms_match_condition(field_keys, terms))


class MergeToOnePipe(object):

    def __init__(
            self,
            source_pipes,
            merge_on_key=lambda entry: entry['ID'],
            key_merge_operation=lambda key_set_a, key_set_b: key_set_a.union(set(key_set_b))):

        self.source_pipes = source_pipes
        self.merge_on_key = merge_on_key
        self.key_merge_operation = key_merge_operation

    def pull(self):

        key_sets = []
        entries = dict()

        for source_pipe in self.source_pipes:
            entry_list = source_pipe.pull().get_entry_list()
            key_set = set()
            for entry in entry_list:
                entry_key = self.merge_on_key(entry)
                entries[entry_key] = entry
                key_set.add(entry_key)
            key_sets.append(key_set)

        merged_keys = reduce(self.key_merge_operation, key_sets)

        bib_data_base = BibDatabase()
        bib_data_base.get_entry_list().extend([entries[key] for key in merged_keys])
        return bib_data_base


class Concatenation(MergeToOnePipe):

    def __init__(self, source_pipes):
        super().__init__(source_pipes)


class MatchTitlesTwoToOnePipe(MergeToOnePipe):
    """
    A merge to one pipe that pulls input from exactly two pipes. Entries from the first pipe are included if their title
    occurs in an entry in the second pipe.
    """
    def __init__(self, source_pipe_a, source_pipe_b):
        def entry_title(entry):
            if 'title' in entry:
                return entry['title'].translate(str.maketrans('', '', string.punctuation)).lower()
            else:
                return None

        super().__init__(
            [source_pipe_a, source_pipe_b],
            entry_title,
            lambda a_keys, b_keys: a_keys.intersection(b_keys))

