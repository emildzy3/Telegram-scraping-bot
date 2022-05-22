import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def get_html_page(url):
    ua = UserAgent().random
    headers = {
        'User-Agent': ua,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
    }
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.text
    print(f'Ошибка - {response.status_code}')

def get_news(url):
    rss = get_html_page(url)
    soup = BeautifulSoup(rss, 'xml')
    list_news = []

    first_three_news = soup.find_all('item')[0:3]
    source_name = soup.find('channel').title.text

    for news in first_three_news:
        title = news.find('title').text
        link = news.find('link').text
        description = news.find('description').text.strip()
        publication_time = ' '.join(news.find('pubDate').text.split(' ')[1:5])

        list_news.append({
            'title': title,
            'link': link,
            'description': description,
            'publication_time': publication_time,
        })

    full_dict_with_name_source = {
        source_name: list_news
    }

    return full_dict_with_name_source


def get_list_news():
    url_ria_rss = 'https://ria.ru/export/rss2/archive/index.xml'
    url_rbc_rss = 'http://static.feed.rbc.ru/rbc/logical/footer/news.rss'
    url_lenta_rss_top7 = 'https://lenta.ru/rss/top7'
    full_list_news = {}
    list_url = [url_rbc_rss, url_ria_rss, url_lenta_rss_top7]
    for url in list_url:
        full_list_news.update(get_news(url))
    return full_list_news


if __name__ == '__main__':
    get_list_news()
