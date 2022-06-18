import requests
from bs4 import BeautifulSoup



def get_html_page(url):
    ua = UserAgent().random
    headers = {
        # 'User-Agent': ua,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
    }

    response = requests.get(url, headers=headers, timeout=5)

    if response.ok:
        return response.text
    print(f'Ошибка - {response.status_code}')


def get_data(data):
    soup = BeautifulSoup(data, 'lxml')
    trs = soup.find('table').find('tbody').find_all('tr')
    crypto_dict = []
    for tr in trs[:3]:
        tds = tr.find_all('td')

        name = tds[2].find('p').text
        price = tds[3].find('a').text.split('$')[-1]

        changes_24_hours_percent = tds[4].find('span').text
        changes_24_hours_up_or_down = tds[4].find('span').span['class'][0].split('-')[-1]
        changes_24_hours = f'{changes_24_hours_up_or_down} {changes_24_hours_percent}'

        crypto_dict.append({
            'name': name,
            'price': price,
            'changes_24_hours': changes_24_hours
        })
    return crypto_dict


def get_crypto_course():
    url = 'https://coinmarketcap.com/'
    return get_data(get_html_page(url))


if __name__ == '__main__':
    get_crypto_course()
