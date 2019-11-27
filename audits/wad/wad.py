import json
import docker


def wad(data):
    try:
        url = data['url']
        client = docker.from_env()
        data = client.containers.run("deep_analize/wad:1.0",
                                     ["wad", "-u", url, "-f", "json"])

        data = json.loads(data)

        for value in data.items():
            data = value[1]
        return data

    except Exception as e:
        print(str(e))
        return 'Not data'
