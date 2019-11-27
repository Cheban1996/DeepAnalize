import os
import time
import requests


def blazy(kwargs):
    url = kwargs['url']
    path = f"{os.getcwd()}/audits/{kwargs['audit']}/"
    with open(path + 'password.txt', 'r') as FILE:
        passwords = FILE.readlines()
        passwords = set([item.replace('\n', '') for item in passwords])
    with open(path + 'username.txt', 'r') as FILE:
        usernames = FILE.readlines()
        usernames = set([item.replace('\n', '') for item in usernames])

    result = []

    for username in usernames:
        for password in passwords:
            req = requests.post(url=url, json={
                'email': username,
                'password': password
            })
            print(req.status_code, username, password)
            if req.status_code == 200:
                result.append({
                    'email': username,
                    'password': password,
                    'response': req.json()
                })
            time.sleep(3)
    return result
