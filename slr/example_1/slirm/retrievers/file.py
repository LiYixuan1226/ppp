from bibtexparser.bparser import BibTexParser


class FileRetriever:

    def __init__(self, input_file):
        self.input_file = input_file


    def pull(self):
        bibtex_parser = BibTexParser(common_strings=True, interpolate_strings = False)
        self.input_file.seek(0)
        return bibtex_parser.parse(self.input_file.read())
