import os

from APICall import APICall

website = {
    "Unsplash": "https://api.unsplash.com/search/photos?",
    "Pexels": "https://api.pexels.com/v1/search?",
}

websiteList = list(website.keys())


class SetUp:
    def __init__(self):
        self.folder = None
        self.key = None
        self.website = None

        self.AskWebsite()
        self.AskFolder()
        temp = APICall(self.key, self.website, self.folder)

    def AskWebsite(self):
        print("Select a website to download from:")
        i = 0
        for key in websiteList:
            print(f"{i}: {key}")
            i += 1
        choice = int(input("Enter a number: "))

        if choice > len(websiteList) or choice < 0:
            print("Invalid choice")
            self.AskWebsite()
        else:
            self.key = websiteList[choice]
            self.website = website[self.key]

    def AskFolder(self):

        folder = input("Enter a folder to save to: ")
        if not os.path.exists(folder):
            print(f"Folder does not exist, creating {folder} folder...")
            os.makedirs(folder)
            print("Folder created")
            self.folder = folder
        else:
            self.folder = folder
