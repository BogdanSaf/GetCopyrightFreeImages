import urllib
from urllib import request
import requests as req


class Unsplash:

    def __init__(self, ):
        self.params = None
        self.requestedPages = None

    def get_header(self):
        headers = {
            'User-Agent': 'student-project/1.0',
            'Content-Type': 'application/json'
        }
        return headers

    def get_params(self, APIKey):
        inputTags = input("Enter tags to search for (add spaces between them): ")
        userTags = {"query": f"{inputTags}"}

        limit = input("Enter how many images you want to download per page (the higher the more time it will spend "
                      "per page): ")
        userLimit = {"per_page": f"{limit}"}

        self.requestedPages = int(input("Enter how many pages you want to download: "))

        userPages = {"page": 1}

        userAPI = {"client_id": f"{APIKey}"}

        self.params = {**userAPI, **userTags, **userLimit, **userPages}
        return self.params

    def get_requestedPages(self):
        return self.requestedPages

    def downloadImages(self, key, folder, JSON_File):
        for images in JSON_File['results']:

            if images['alt_description'] is None:
                description = "No description"
            else:
                description = images['alt_description']

            url = images['urls']['full']

            uploadedBy = images['user']['name']

            imageType = images['urls']['full'].split('.')[-1]

            print("Downloading image: " + description + " uploaded by " + uploadedBy + " from " + key + "...")
            urllib.request.urlretrieve(url,
                                       folder + "/ (Unsplash)_" + description + "uploaded by " + uploadedBy + "."
                                       + "jpg")

    def startDownload(self, key, folder, JSON_File, requestedPages, params, headers):
        currentPages = 1

        requestedPages = int(requestedPages)
        params = params
        totalPages = JSON_File['total_pages']

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
            response = client.get("https://api.unsplash.com/search/photos?", headers=headers, params=params)
            self.downloadImages("Unsplash", folder, response.json())
            currentPages += 1
