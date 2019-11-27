import docker


def brutex(kwargs):
    url = kwargs['result']
    client = docker.from_env()
    data = client.containers.run("deep_analize/brutex:1.0",
                                 list_command,
                                 detach=True)
