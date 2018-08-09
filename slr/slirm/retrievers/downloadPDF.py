import urllib.request
import os

class DownloadPDF(object):
    def __init__(self, lists, count, path):
        self.lists = lists
        self.count = count
        self.path = path

    def download(self):  # 下载文件
        i = 0
        for record in self.lists:
            if i >= self.count:
                break
            url = str(record['pdf_url'])
            file_name = str(record['title']) + ".pdf"
            file_name = file_name.replace(" ", "_")
            dest_dir = os.path.join(self.path, file_name)
            print(dest_dir)
            print(url)
            print(file_name)
            self.urlretrieveMethod(dest_dir, url)
            i += 1

    def urlretrieveMethod(self, dest_dir, url):  # 下载文件的专属函数
        try:
            urllib.request.urlretrieve(url, dest_dir)
        except:
            print('\tError retrieving the URL:', dest_dir)

