import unittest

from slirm.filter.automatic import DuplicateEntryFilter
from slirm.retrievers.file import FileRetriever


class ExcludeDuplicatesTest(unittest.TestCase):

    def test_exclude_duplicates(self):
        with open('tests/test_exclude_duplicates.bib') as duplicates_file:

            duplicates = FileRetriever(duplicates_file)
            duplicate_entry_filter = DuplicateEntryFilter(duplicates)
            unique_entries = duplicate_entry_filter.pull().get_entry_list()

            self.assertEquals(2, len(unique_entries))


if __name__ == '__main__':
    unittest.main()
