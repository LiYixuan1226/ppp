import unittest

from slirm.retrievers.ScienceDirect import ScienceDirectRetrieve

from bibtexparser.bwriter import BibTexWriter


class ScienceDirectRetrieveTestCase(unittest.TestCase):

    def test_retrieve(self):

        query = 'software testing'
        api_key = '5b8627370566798169844f272c6af106'
        sd_retrieve = ScienceDirectRetrieve([query], api_key)
        bibtex_database = sd_retrieve.pull()

        self.assertGreater(len(bibtex_database), 0)


if __name__ == '__main__':
    unittest.main()