import urllib
from math import floor
from urllib import request
import requests as req


class Pixabay:
    def __init__(self):
        self.folder = None
        self.headers = None
        self.params = None
        self.requestedPages = 0

    def get_params(self, APIKey):
        inputTags = input("Enter tags to search for (add spaces between them): ")
        userTags = {"q": f"{inputTags}"}

        limit = input("Enter how many images you want to download per page (the higher the more time it will spend "
                      "per page): ")
        userLimit = {"per_page": f"{limit}"}

        self.requestedPages = int(input("Enter how many pages you want to download: "))

        userPages = {"page": 1}

        userAPI = {"key": f"{APIKey}"}

        self.params = {**userAPI, **userTags, **userPages, **userLimit}
        return self.params

    def get_requestedPages(self):
        return self.requestedPages

    def get_header(self):
        self.headers = {
            'User-Agent': 'student-project/1.0',
            'Content-Type': 'application/json'
        }
        return self.headers

    def downloadImages(self, key, folder, JSON_File):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', 'student-project/1.0')]
        urllib.request.install_opener(opener)
        for images in JSON_File['hits']:

            if images['tags'] is None:
                description = "No description"
            else:
                description = images['tags']

            url = images['largeImageURL']

            uploadedBy = images['user']

            imageType = images['largeImageURL'].split('.')[-1]

            print("Downloading image: " + description + " uploaded by " + uploadedBy + " from " + key + "...")
            urllib.request.urlretrieve(url,
                                       folder + "/ (Pixabay)_" + description + "uploaded by " + uploadedBy + "."
                                       + imageType)

    def startDownload(self, key, folder, JSON_File, requestedPages, params, headers):
        currentPages = 1

        requestedPages = int(requestedPages)
        params = params
        totalPages = floor(JSON_File['totalHits'] / int(params['per_page']))

        if requestedPages > totalPages:
            print("You requested more pages than there are, setting it to the max amount of pages")
            print("Max amount of pages: " + str(totalPages))
            answer = input("Do you want to set that as the maximum or enter a new amount? (y/n): ")

            if answer == "y":
                self.requestedPages = totalPages
            elif answer == "n":
                requestedPages = int(input("Enter how many pages do you want to download: "))
                self.startDownload(key, folder, JSON_File, requestedPages, params, headers)

        print("Total pages: " + str(totalPages) + " Requested pages: " + str(requestedPages))

        while currentPages <= requestedPages:
            client = req.Session()
            client.headers.update(headers)
            params['page'] = currentPages
            response = client.get("https://pixabay.com/api/", headers=headers, params=params)
            self.downloadImages("Pixabay", folder, response.json())
            currentPages += 1