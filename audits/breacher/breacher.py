import docker
from main import Docker


def breacher(data):
    url = data['url']
    client = docker.from_env()
    data = client.containers.run("deep_analize/breacher:1.0", ['-u', url])
    data = data.decode('utf-8')
    useful_data = data.split('\n')

    find_url = []
    for i in useful_data:
        if '+' in i:
            find_url.append(i.replace('[1;32m[+][0m', ''))

    return find_url
