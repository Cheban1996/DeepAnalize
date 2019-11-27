import requests
from bs4 import BeautifulSoup

from primitives import validate_domain

SITE_CHECK = 'http://www.topsimilarsites.com/similar-to/'


def similar_site(data):
    url = validate_domain(data['url'])
    target = requests.get(SITE_CHECK + url)
    text = target.text
    soup = BeautifulSoup(text, 'html.parser')
    alternative = []
    for i in soup.find_all('span', class_='name'):
        alternative.append(i.a.get_text())

    name_domain = validate_domain(url)
    name = ''
    for i in range(len(name_domain)):
        if name_domain[i] == '.':
            name = name_domain[:i]

    similar_list = []
    new_alternative = []
    for i in alternative:
        if name.lower() in i.lower():
            similar_list.append(i)
        else:
            new_alternative.append(i)
    del alternative

    return {
        'alternative': new_alternative,
        'similar': similar_list}
