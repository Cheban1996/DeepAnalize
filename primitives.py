import codecs
import json
from typing import Optional
from bs4 import BeautifulSoup
import requests
import chardet


def validate_url(url: str):
    if 'http://' in url or 'https://' in url:
        return url
    else:
        return 'http://' + url


def validate_domain(domain: str):
    if 'https://' in domain:
        return domain[8:]
    elif 'http://' in domain:
        return domain[7:]
    else:
        return domain


def reverse_domain(url: str):
    if 'https' in url:
        url = url[8:]

    if 'http' in url:
        url = url[7:]

    if 'www' in url:
        url = url[4:]

    i = 0
    while i < len(url):
        if url[i] == '/':
            url = url[:i]
            break
        i += 1

    return url


def extract_sb_count(soup):
    sb_count_select = soup.select('span.sb_count')
    sb_count_tag = sb_count_select[0] if sb_count_select else None
    if sb_count_tag is None:
        return None
    sb_count = None
    if sb_count_tag:
        sb_count = ''.join(filter(lambda c: c.isdigit(), sb_count_tag.text))
        sb_count = int(sb_count)
    return


def convert_name(name):
    name = name.replace('_', ' ')
    name = name.title()
    name = name.replace(' ', '')
    return name


def parse_json(content, **kwargs):
    """Returns the object from parsed json content, if any.
    Raises:
        ValueError: If the response body does not contain valid json.
    """

    if not isinstance(content, str) and content and len(content) > 3:
        # No encoding set. JSON RFC 4627 section 3 states we should expect
        # UTF-8, -16 or -32. Detect which one to use; If the detection or
        # decoding fails, fall back to using chardet to make
        # a best guess.
        encoding = guess_json_utf(content)
        if encoding is not None:
            try:
                return json.loads(content.decode(encoding), **kwargs)
            except UnicodeDecodeError:
                # Wrong UTF codec detected; usually because it's not UTF-8
                # but some other 8-bit codec.  This is an RFC violation,
                # and the server didn't bother to tell us what codec *was*
                # used.
                encoding = chardet.detect(content)['encoding']
                return json.loads(content.decode(encoding), **kwargs)
    return json.loads(content, **kwargs)


# Null bytes; no need to recreate these on each call to guess_json_utf
_null = '\x00'.encode('ascii')  # encoding to ASCII for Python 3
_null2 = _null * 2
_null3 = _null * 3


def guess_json_utf(data) -> Optional[str]:
    # JSON always starts with two ASCII characters, so detection is as
    # easy as counting the nulls and from their location and count
    # determine the encoding. Also detect a BOM, if present.
    sample = data[:4]
    if sample in (codecs.BOM_UTF32_LE, codecs.BOM32_BE):
        return 'utf-32'  # BOM included
    if sample[:3] == codecs.BOM_UTF8:
        return 'utf-8-sig'  # BOM included, MS style (discouraged)
    if sample[:2] in (codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE):
        return 'utf-16'  # BOM included
    nullcount = sample.count(_null)
    if nullcount == 0:
        return 'utf-8'
    if nullcount == 2:
        if sample[::2] == _null2:  # 1st and 3rd are null
            return 'utf-16-be'
        if sample[1::2] == _null2:  # 2nd and 4th are null
            return 'utf-16-le'
            # Did not detect 2 valid UTF-16 ascii-range characters
    if nullcount == 3:
        if sample[:3] == _null3:
            return 'utf-32-be'
        if sample[1:] == _null3:
            return 'utf-32-le'
            # Did not detect a valid UTF-32 ascii-range character
    return None


def sort_to_ver(ver: str) -> str:
    point = 0
    for i in range(len(ver)):
        if ver[i] == '.':
            point += 1
            if point == 2:
                return f' {ver[:i]}'


def div_pdf(id):
    addr = "http://127.0.0.1:8001/id/" + id
    r = requests.get(addr)
    soup = BeautifulSoup(r.text, 'html.parser')
    div = soup.find('div', id='content')
    return div
