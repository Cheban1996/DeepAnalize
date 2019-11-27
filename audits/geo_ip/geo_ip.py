import csv
import ipaddress
import os

from deepanalize.audits.audit.get_ip import get_ip

current_dir = os.path.abspath(os.path.dirname(__file__))


def geo_ip(url):
    ip = get_ip.run(url)

    file_name = os.path.join(current_dir, 'GeoIPCountryWhois.csv')  # datebase csv range ip

    ip_int = int(ipaddress.IPv4Address(ip))  # int ip
    ip_country = 'None'
    flag = 'None'
    with open(file_name, 'r', newline='') as file:
        read = csv.reader(file)
        for i in read:
            if ip_int >= int(i[2]) and ip_int <= int(i[3]):
                flag = i[4]
                ip_country = i[5]
                break

    code = f'ISO 3166-1 {flag}'

    return {
        'code': code,
        'country': ip_country
    }
