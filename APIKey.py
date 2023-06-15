import json
import os


class APIKey:
    def __init__(self, key):
        data = {}
        if os.path.exists("API.json") and os.path.getsize("API.json") > 0:
            with open("API.json", "r") as file:

                data = json.load(file)

                if key + "Key" in data:
                    self.websiteAPIKey = data[key + "Key"]
                else:
                    self.ask_for_key(key, data)
        else:
            self.ask_for_key(key, data)

    def ask_for_key(self, key, data):
        print("API.json file not found, or empty")
        print(f"Warning: You will not be able to download images from {key} without an API key")
        self.websiteAPIKey = input("Enter your API key: ")
        answer = input("Do you want to save this key? (y/n): ")
        if answer == "y":
            answerSure = input(
                "Are you sure? The file will not be encrypted and everyone accessing the JSON file will be able to "
                "see it (y/n): ")

            if answerSure == "y":
                with open("API.json", "w") as file:
                    data[key + "Key"] = self.websiteAPIKey
                    json.dump(data, file, indent=4, sort_keys=True)
                    print("API key saved")
            elif answerSure == "n":
                print("API key not saved. You will have to enter it again next time you run the program")
            else:
                print("Invalid answer")
                self.ask_for_key(key, data)

        elif answer == "n":
            print("API key not saved. You will have to enter it again next time you run the program")
        else:
            print("Invalid answer")
            self.ask_for_key(key, data)

    def get_key(self):
        return self.websiteAPIKey
