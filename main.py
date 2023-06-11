import json
import os
import urllib
import urllib.request
import requests as req
import urllib.parse
from PIL import Image

website = {
    "Unsplash": "https://api.unsplash.com/search/photos?",
}

websiteList = list(website.keys())


class AskWebsite:
    def __init__(self):
        print("Select a website to download from:")
        i = 0
        for key in websiteList:
            print(f"{i}: {key}")
            i += 1
        choice = int(input("Enter a number: "))

        if choice > len(websiteList) or choice < 0:
            print("Invalid choice")
            AskWebsite()

        self.choice = choice


class AskFolder:
    def __init__(self):
        folder = input("Enter a folder to save to: ")
        if not os.path.exists(folder):
            print("Folder does not exist, creating local images folder...")
            os.makedirs(folder)
            print("Folder created")
            self.folder = folder
        else:
            self.folder = folder


class APIKey:
    def __init__(self):
        if os.path.exists("API.json") and os.path.getsize("API.json") > 0:
            with open("API.json", "r") as file:
                data = json.load(file)
                self.key = data["key"]
        else:
            self.ask_for_key()

    def ask_for_key(self):
        print("API.json file not found, or empty")
        print("Warning: You will not be able to download images from Unsplash without an API key")
        self.key = input("Enter your API key: ")
        answer = input("Do you want to save this key? (y/n): ")
        if answer == "y":
            answerSure = input(
                "Are you sure? The file will not be encrypted and everyone accessing the JSON file will be able to see it (y/n): ")

            if answerSure == "y":
                with open("API.json", "w") as file:
                    json.dump({"key": self.key}, file)
                    print("API key saved")
            elif answerSure == "n":
                print("API key not saved. You will have to enter it again next time you run the program")
            else:
                print("Invalid answer")
                self.ask_for_key()

        elif answer == "n":
            print("API key not saved. You will have to enter it again next time you run the program")
        else:
            print("Invalid answer")
            self.ask_for_key()


class AskParams:
    def __init__(self):
        inputTags = input("Enter tags to search for (add spaces between them): ")
        self.userTags = {"query": f"{inputTags}"}

        limit = input("Enter how many images you want to download per page (the higher the more time it will spend "
                      "per page): ")
        self.userLimit = {"limit": f"{limit}"}

        self.requestedPages = int(input("Enter how many pages you want to download: "))

        self.userPages = {"page": 1}

        api = APIKey()
        self.userAPI = {"client_id": f"{api.key}"}

        self.params = {**self.userAPI, **self.userTags, **self.userLimit, **self.userPages}


# Gets the images
class APICall:
    def __init__(self, choice, params):
        urlBase = website[websiteList[choice]]
        headers = {'User-Agent': 'student-project/1.0',
                   'Content-Type': 'application/json'
                   }

        method = 'GET'
        self.client = req.Session()
        self.client.headers.update(headers)
        self.response = self.client.request(method, urlBase, headers=headers, params=params)

    def get_status(self):
        return self.response.status_code

    def get_json(self):
        return self.response.json()

    def get_content(self):
        return self.response.content

    def get_x_ratelimit_remaining(self):
        return self.response.headers.get('X-Ratelimit-Remaining')

    def get_x_ratelimit_reset(self):
        return self.response.headers.get('X-Ratelimit-Reset')


class Download_Images:
    def __init__(self, folder, JSON_File):
        for images in JSON_File['results']:

            if images['alt_description'] is None:
                description = "No description"
            else:
                description = images['alt_description']

            url = images['urls']['full']

            uploadedBy = images['user']['name']

            imageType = images['urls']['full'].split('.')[-1]

            print("Downloading image: " + description + " uploaded by " + uploadedBy + " from " + websiteList[
                userAnswer.choice] + "...")
            urllib.request.urlretrieve(url,
                                       folder + "/ (Unsplash)_" + description + "uploaded by " + uploadedBy + "."
                                       + imageType)


if __name__ == '__main__':
    userAnswer = AskWebsite()
    params = AskParams()
    folder = AskFolder().folder

    api = APICall(userAnswer.choice, params.params)

    if api.get_status() != 200:
        print("Doesnt work! Status code: " + str(api.get_status()))

    if api.get_x_ratelimit_remaining() == 0:
        print("Rate limit reached")
        print("Rate limit resets in " + str(api.get_x_ratelimit_remaining()) + " seconds")
        exit()
    else:
        print("Rate limit remaining: " + str(api.get_x_ratelimit_remaining()))
        print("Rate limit resets in " + str(api.get_x_ratelimit_reset()) + " seconds")

    if api.get_json()['total'] == 0:
        print("No results found")
        exit()

    number_of_pages = int(api.get_json()['total_pages'])

    currentPage = 1

    userPages = int(params.requestedPages)

    while currentPage <= userPages <= number_of_pages:
        params.params['page'] = currentPage
        api2 = APICall(userAnswer.choice, params.params)
        Download_Images(folder, api2.get_json())
        currentPage += 1
