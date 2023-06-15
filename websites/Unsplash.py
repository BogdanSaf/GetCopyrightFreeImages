import urllib
from urllib import request


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

        api = APIKey
        userAPI = {"client_id": f"{api}"}

        self.params = {**userAPI, **userTags, **userLimit, **userPages}
        return self.params

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
                                       + imageType)
