import socket
from primitives import validate_domain


def get_ip(data):
    try:
        url = validate_domain(data['url'])
        ip = socket.gethostbyname(url)
        return ip
    except Exception:
        return 'Not found'
