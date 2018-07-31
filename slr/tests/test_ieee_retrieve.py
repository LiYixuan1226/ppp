import unittest

from slirm.retrievers.ieee_xplore import IEEEXploreRetrieve

from bibtexparser.bwriter import BibTexWriter


class IEEEXploreRetrieveTestCase(unittest.TestCase):

    def test_retrieve(self):

        query = 'software testing'
        api_key = 'xxbuhzj7q5zfednrb9j49yzq'
        ieee_xplore_retrieve = IEEEXploreRetrieve([query], api_key)
        bibtex_database = ieee_xplore_retrieve.pull()

        self.assertGreater(len(bibtex_database.get_entry_list()), 0)


if __name__ == '__main__':
    unittest.main()
