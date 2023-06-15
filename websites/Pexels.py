import urllib
from math import floor
from urllib import request
import requests as req


class Pexels:
    def __init__(self):
        self.folder = None
        self.headers = None
        self.params = None
        self.requestedPages = 0

    def get_params(self):
        inputTags = input("Enter tags to search for (add spaces between them): ")
        userTags = {"query": f"{inputTags}"}

        limit = int(input("Enter how many images you want to download per page (the higher the more time it will spend "
                          "per page): "))

        if limit is None:
            limit = 15
        elif limit > 80:
            print("The limit is 80, setting it to 80")
            limit = 80

        userLimit = {"per_page": f"{limit}"}

        self.requestedPages = int(input("Enter how many pages do you want to download: "))
        print(self.requestedPages)

        userPages = {"page": 1}

        self.params = {**userTags, **userLimit, **userPages}
        return self.params

    def get_requestedPages(self):
        return self.requestedPages

    def get_header(self, APIKey):
        self.headers = {
            'Authorization': f"{APIKey}",
            'User-Agent': 'student-project/1.0',
            'Content-Type': 'application/json'
        }
        return self.headers

    def downloadImages(self, key, folder, JSON_File):
        self.folder = folder
        opener = urllib.request.build_opener()
        opener.addheaders = [('Authorization', key)]
        urllib.request.install_opener(opener)

        for images in JSON_File['photos']:
            if images['alt'] is None:
                description = "No description"
            else:
                description = images['alt']

            url = images['src']['original']

            uploadedBy = images['photographer']

            imageType = images['src']['original'].split('.')[-1]

            print("Downloading image: " + description + " uploaded by " + uploadedBy + " from " + key + "...")
            urllib.request.urlretrieve(url,
                                       folder + "/ (Pexels)_" + description + "uploaded by " + uploadedBy + "."
                                       + imageType)

    def getPages(self, key, folder, JSON_File, requestedPages, params, headers):

        currentPages = 1

        requestedPages = int(requestedPages)
        params = params
        totalPages = floor(JSON_File['total_results'] / JSON_File['per_page'])

        if requestedPages > totalPages:
            print("You requested more pages than there are, setting it to the max amount of pages")
            print("Max amount of pages: " + str(totalPages))
            answer = input("Do you want to set that as the maximum or enter a new amount? (y/n): ")

            if answer == "y":
                self.requestedPages = totalPages
            elif answer == "n":
                requestedPages = int(input("Enter how many pages do you want to download: "))
                self.checkPagesLeft(key, folder, JSON_File, requestedPages, params)

        print("Total pages: " + str(totalPages) + " Requested pages: " + str(requestedPages))

        while currentPages <= requestedPages:
            client = req.Session()
            client.headers.update(headers)
            params['page'] = currentPages
            response = client.get("https://api.pexels.com/v1/search?", headers=headers, params=params)
            self.downloadImages("Pexels", folder, response.json())
            currentPages += 1
