import socket
import requests

from primitives import validate_domain


def nmap_port(data):
    ip = socket.gethostbyname(validate_domain(data['url']))
    response = requests.get(f'http://api.hackertarget.com/nmap/?q={ip}')
    return response.text
