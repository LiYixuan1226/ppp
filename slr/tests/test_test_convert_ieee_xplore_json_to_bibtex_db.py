import unittest

from slirm.retrievers.ieee_xplore import convert_ieee_xplore_json_to_bibtex_db
from bibtexparser.bwriter import BibTexWriter


class ConvertIEEEXploreJSONToBibTeXTestCase(unittest.TestCase):

    def test_convert_ieee_xplore_json_to_bibtex_db(self):

        with \
                open('convert_ieee_xplore_json_to_bibtex_db_test.json') as test_input_file, \
                open('convert_ieee_xplore_json_to_bibtex_db_test.bib') as test_output_file:
            json_string = test_input_file.read()

            bibtex_database = convert_ieee_xplore_json_to_bibtex_db(json_string)

            bibtex_writer = BibTexWriter()

            self.assertEquals(test_output_file.read(), bibtex_writer.write(bibtex_database))


if __name__ == '__main__':
    unittest.main()
