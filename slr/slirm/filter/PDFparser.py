from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import *
from pdfminer.converter import PDFPageAggregator
import os

fp = open('python.pdf', 'rb')
parser = PDFParser(fp)
document = PDFDocument(parser)
if not document.is_extractable:
    raise PDFTextExtractionNotAllowed
else:
    rsrcmgr=PDFResourceManager()
    laparams=LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        for x in layout:
              if (isinstance(x, LTTextBoxHorizontal)):
                 with open('a.txt', 'a') as f:
                    f.write(str(x.get_text().encode('utf-8')))
