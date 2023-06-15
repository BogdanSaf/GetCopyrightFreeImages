import urllib
from urllib import request


class Pexels:
    def __init__(self):
        self.headers = None
        self.params = None
        self.requestedPages = None

    def get_params(self):
        inputTags = input("Enter tags to search for (add spaces between them): ")
        userTags = {"query": f"{inputTags}"}

        limit = input("Enter how many images you want to download per page (the higher the more time it will spend "
                      "per page): ")
        userLimit = {"per_page": f"{limit}"}

        self.requestedPages = int(input("Enter how many pages you want to download: "))

        userPages = {"page": 1}

        self.params = {**userTags, **userLimit, **userPages}
        return self.params

    def get_header(self, APIKey):
        self.headers = {
            'Authorization': f"{APIKey}",
            'User-Agent': 'student-project/1.0',
            'Content-Type': 'application/json'
        }
        return self.headers

    def downloadImages(self, key, folder, JSON_File):
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
