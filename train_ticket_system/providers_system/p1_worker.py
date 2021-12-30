import requests
import pandas as pd


class Provider1Worker:
    def __init__(self):
        self.endpoint = "http://127.0.0.1:8081/search"

    def get_all(self):
        response = requests.get(self.endpoint)
        temp = pd.DataFrame(response.json(), dtype=str)
        temp["provider_id"] = ["1" for x in range(len(temp))]
        return temp

    def get_by(self, args):
        endpoint = self.endpoint + "?"
        for key, value in args.items():
            endpoint = endpoint + key + "=" + value + "&"
        response = requests.get(endpoint[:-1])
        temp = pd.DataFrame(response.json(), dtype=str)
        temp["provider_id"] = ["1" for x in range(len(temp))]
        return temp
