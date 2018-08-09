import ieee_xplore
import downloadPDF
import json

def main():
    #query = 'software testing'
    query = list()
    api_key = 'xxbuhzj7q5zfednrb9j49yzq'
    # keyword = input("What key words do you want to search: ")
    # query.append(keyword)
    # author = input("Who is the author you are looking for: ")
    # query.append(author)
    # path = input("Please input download path:")
    with open('IEEE', 'r') as f:
        f_dict = json.load(f)
    for key in f_dict:
        if key == 'file':
            path = f_dict[key]
            continue
        if f_dict[key] != '':
            query.append(str(f_dict[key]).replace(" ","_"))

    ieee_retrieve = ieee_xplore.IEEEXploreRetrieve(query, api_key, maximum_results=1000)
    bibtex_database, lists, count = ieee_retrieve.pull()
    print("Number of eligible documents："+ str(count))
    downloader = downloadPDF.DownloadPDF(lists, count, path)
    downloader.download()
    print(bibtex_database)

if __name__ == '__main__':
    main()