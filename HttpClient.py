import json

import requests
import urllib3
from http3 import Response


class HttpClient:
    @staticmethod
    def get_request(url: str, params: dict) -> Response:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(url, params, verify=False)
        return response.json()
