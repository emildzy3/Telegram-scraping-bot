import requests

from exception import CantConnectToServer


def get_html_page(url: str) -> str:
    """Service for receiving HTML/XML pages"""
    headers = _get_user_agent()
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.text
    raise CantConnectToServer


def _get_user_agent() -> dict[str, str]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
    }
    return headers


if __name__ == '__main__':
    print(get_html_page('https://ria.ru/export/rss2/archive/index.xml'))
