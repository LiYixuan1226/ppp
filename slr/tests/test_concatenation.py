import unittest

from slirm.filter.automatic import Concatenation
from slirm.retrievers.file import FileRetriever


class ConcatenationTest(unittest.TestCase):

    def test_concatenation(self):
        """
        Reads two files that contain 27 entries, of which 2 are duplicates that occur in both files.  Tests that 25
        uniques entries are passed on when the two files are merged.
        """
        with \
                open('test_concatenation_a.bib') as test_file_a, \
                open('test_concatenation_b.bib') as test_file_b:

            file_retriever_a = FileRetriever(test_file_a)
            file_retriever_b = FileRetriever(test_file_b)

            concatenation = Concatenation([file_retriever_a, file_retriever_b])

            concatenation_database = concatenation.pull()

            self.assertEquals(25, len(concatenation_database.get_entry_list()))


if __name__ == '__main__':
    unittest.main()
