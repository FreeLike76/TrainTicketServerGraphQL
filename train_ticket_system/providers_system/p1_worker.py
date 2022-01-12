import requests
import pandas as pd


class Provider1Worker:
    def __init__(self):
        self.endpoint = "http://127.0.0.1:8081/search"

    def get_all(self):
        response = requests.get(self.endpoint)
        temp = pd.DataFrame(response.json(), dtype=str)
        temp["provider_id"] = "1"
        return temp
