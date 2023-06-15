import urllib
from urllib import parse

import requests as req

from APIKey import APIKey
from websites.Pexels import Pexels
from websites.Unsplash import Unsplash


class APICall:
    def __init__(self, key, website, folder):
        self.client = None
        self.response = None
        self.key = key
        self.website = website
        self.folder = folder
        self.apiKey = APIKey(key).get_key()
        self.choseWebsite()

    def choseWebsite(self):
        match self.key:
            case "Unsplash":
                params = Unsplash().get_params(self.apiKey)
                headers = Unsplash().get_header()
                self.apiCall(params, headers, self.website)

                if self.get_status() == 200:
                    Unsplash().downloadImages(self.key, self.folder, self.get_json())
                else:
                    print("Error: " + str(self.get_status()))
                    exit()
            case "Pexels":
                params = Pexels().get_params()
                headers = Pexels().get_header(self.apiKey)
                print(headers['Authorization'])
                self.apiCall(params, headers, self.website)

                if self.get_status() == 200:
                    Pexels().downloadImages(self.key, self.folder, self.get_json())
                else:
                    print("Error: " + str(self.get_status()))
                    exit()
            case _:
                print(f"Error: Invalid website. Looks like we don't support {self.key} yet.")
                exit()

    def apiCall(self, params, headers, website):
        urlBase = website
        print(urlBase + urllib.parse.urlencode(params))
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
