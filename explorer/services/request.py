import json
import requests
from django.conf import settings


def json_rpc(method: str, params=list, endpoint='', authorisation=''):
    headers = {
        'Content-Type': 'application/json',
    }

    if authorisation:
        headers['Authorization'] = authorisation

    data = {
        'jsonrpc': '2.0',
        'method': method,
        'params': params
    }

    if not endpoint:
        endpoint = settings.NODE_PROVIDERS['quicknode']['endpoint']

    response = requests.post(endpoint, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        data = response.json()
        return data['result']
    else:
        raise requests.HTTPError(f"Request failed with status message: {response.text}")


def get_request(endpoint: str):
    response = requests.get(endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        raise requests.HTTPError(f"Request failed with status message: {response.text}")
