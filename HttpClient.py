import requests


class HttpClient:
    @staticmethod
    def get_request(url: str, params: dict):
        response = requests.get(url, params, verify=False)
        return response.json()
