from bs4 import BeautifulSoup
import requests
from deepanalize.audits.audit.get_ip import get_ip


def bing_ip(url: str):
    try:
        ip = get_ip.run(url)
        r = requests.get(f'https://www.bing.com/search?q=IP%3A{ip}')
        soup = BeautifulSoup(r.text, 'html.parser')
        sb_count = soup.find_all(class_='sb_count')
        sb_count = sb_count[0].get_text()
        number = sb_count.split(' ')
        number = int(number[0])  # how many site on domain
        number = int(number / 10)
        count = 1
        list_link = []
        for i in range(1, number + 2):
            r = requests.get(f'https://www.bing.com/search?q=IP%3a{ip}&first={count}&format=rss')
            soup = BeautifulSoup(r.text, 'xml')
            for j in soup.find_all('item'):
                link = j.find('link')
                list_link.append(link.get_text())
            count += 10
        if len(list_link) == 0:
            return 'Not Found'
        else:
            return {
                'ip': ip,
                'list_link': list_link,
            }

    except Exception as e:
        print(e)
        return 'Not Found'
