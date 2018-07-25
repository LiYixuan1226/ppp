import os
import unittest

from slirm.filter.interactive import InteractiveFilter, CIUserInterface
from slirm.retrievers.file import FileRetriever


class InteractiveTestCase(unittest.TestCase):

    def test_interactive(self):
        with \
                open('tests/test_interactive.bib', mode='r') as input_file, \
                open('tests/test_interactive_included_keys_file.txt', mode='a') as included_keys_file, \
                open('tests/test_interactive_excluded_keys_file.txt', mode='a') as excluded_keys_file:

            file_retriever = FileRetriever(input_file)

            db = InteractiveFilter(
                file_retriever,
                CIUserInterface(),
                included_keys_file,
                excluded_keys_file).pull()

    def tearDown(self):
        os.remove('tests/test_interactive_included_keys_file.txt')
        os.remove('tests/test_interactive_excluded_keys_file.txt')

if __name__ == '__main__':
    unittest.main()


