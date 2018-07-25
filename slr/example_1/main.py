from slirm.retrievers import FileRetriever, CachingRetriever
from slirm.filter import Concatenation, DateRangeFilter, DuplicateEntryFilter, ExcludeKeysFilter, ExcludeTermFilter, \
    IncludeKeysFilter
from slirm.requesters import FileWriterRequester
from slirm.filter import CountEntries
from slirm.filter import CIUserInterface, InteractiveFilter
from datetime import date
import string

import logging
logging.basicConfig(level=logging.INFO)


def entry_title(entry):
    if 'title' in entry:
        return entry['title'].translate(str.maketrans('', '', string.punctuation)).lower()
    else:
        return None


with open('included_keys.txt', mode='r', encoding='utf-8') as included_keys_file:
    included_keys = set(included_keys_file.read().split("\n"))

with open('excluded_keys.txt', mode='r', encoding='utf-8') as excluded_keys_file:
    excluded_keys = set(excluded_keys_file.read().split("\n"))

with \
        open('Stage1.bib', mode='r', encoding='utf-8') as stage_1_file, \
        open('included_keys.txt', mode='a', encoding='utf-8') as included_keys_file, \
        open('excluded_keys.txt', mode='a', encoding='utf-8') as excluded_keys_file, \
        open('slr.bib', encoding='utf-8', mode='w', newline='') as found_file:

    file_retriever = CachingRetriever(FileRetriever(stage_1_file))

    stage_1_count = CountEntries(file_retriever, "Found [%d] entries in the file.")

    duplicate_key_filter = DuplicateEntryFilter(stage_1_count, entry_title)

    stage_2_count = CountEntries(duplicate_key_filter, "Found [%d] after removing duplicates.")

    date_range_filter = DateRangeFilter(stage_2_count, date(2000, 1, 1), date(2018, 12, 31))

    stage_3_count = CountEntries(date_range_filter, "Found [%d] entries after filtering dates.")


    terms = [
        'Chemical',
        'Chromatography',
        'Electromagnetic',
        'Electronic',
        'Transmission',
        'Geography',
        'Microwave',
        'Bio',
        'Surg',
        'Building',
        'Law',
        'Ocean',
        'Alco',
        'Genetics',
        'Carbon',
        'Electronic',
        'Dataware',
        'Chapter',
        'Robot',
        'Medicine']

    fields = ['keywords', 'journal', 'booktitle', 'title']

    term_filter = ExcludeTermFilter(stage_3_count, fields, terms)

    stage_4_count = CountEntries(term_filter, "Found [%d] entries after filtering on keywords.")

    excluded_key_filter = ExcludeKeysFilter(stage_4_count, excluded_keys)

    included_keys_filter = IncludeKeysFilter(CachingRetriever(excluded_key_filter), included_keys)

    user_interface = CIUserInterface()

    interactive_filter = InteractiveFilter(included_keys_filter.no_match_pipe(), user_interface, included_keys_file, excluded_keys_file)

    stage_5_1_count = CountEntries(interactive_filter, "Found [%d] entries after interactive review.")
    stage_5_2_count = CountEntries(included_keys_filter, "Found [%d] entries already reviewed.")

    concatenation = Concatenation([stage_5_1_count, stage_5_2_count])

    stage_6_count = CountEntries(concatenation)



    found_writer = FileWriterRequester(stage_6_count, found_file)
    found_writer.request()
