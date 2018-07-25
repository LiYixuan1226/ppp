from bibtexparser.bwriter import BibTexWriter


class FileWriterRequester(object):

    def __init__(self, source_pipe, out_file):
        self.source_pipe = source_pipe
        self.out_file = out_file

    def request(self):
        bibtex_writer = BibTexWriter()
        self.out_file.write(bibtex_writer.write(self.source_pipe.pull()))
