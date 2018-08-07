import requests

class Download(object):
    def download(url, path):
        url = '//www.jb51.net/test/demo.zip'
        r = requests.get(url)
        with open("path", "wb") as code:
            code.write(r.content)
