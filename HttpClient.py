import requests
import urllib3


class HttpClient:
    @staticmethod
    def get_request(url: str, params: dict):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(url, params, verify=False)
        return response.json()
