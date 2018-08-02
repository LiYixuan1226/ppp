import unittest

from slirm.retrievers.springerlink import SpringerLinkRetrieve

from bibtexparser.bwriter import BibTexWriter


class SpringerlinkRetrieveTestCase(unittest.TestCase):

    def test_retrieve(self):

        query = 'software testing'
        api_key = 'a6cb064309bb238a35a383a30f510748'
        springerlink_retrieve = SpringerLinkRetrieve([query], api_key)
        bibtex_database = springerlink_retrieve.pull()

        self.assertGreater(len(bibtex_database), 0)


if __name__ == '__main__':
    unittest.main()
