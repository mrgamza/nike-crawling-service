import requests

from nike_crawling_service.util import Properties


def get_html(url):
    resp = requests.get(url, headers={
        'User-Agent': Properties.userAgent,
        'Accept-Language': 'ko-KR',
        'Accept': 'text/html'
    })

    if resp.status_code == 200:
        return resp
    return None

