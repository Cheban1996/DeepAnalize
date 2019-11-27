import os
import requests


def api_corn(kwargs):
    url = kwargs['url']

    path_package = f"{os.getcwd()}/audits/{kwargs['audit']}/"
    with open(path_package + 'path.txt', 'r') as FILE:
        path_resource = FILE.readlines()
        path_resource = [item.replace('\n', '') for item in path_resource]

    result = {}

    for path in path_resource:
        req = requests.post(url=f"{url}/{path}")

        if req.status_code != 404:
            result.update({
                'url': url,
                'response': req.json()
            })
    return result