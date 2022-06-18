from dataclasses import dataclass
from datetime import datetime

from bs4 import BeautifulSoup, ResultSet

from exception import CantGetNews
from settings import COUNT_NEWS

Url = str


@dataclass
class News:
    title: str
    publication_time: datetime
    description: str
    link_news: Url


@dataclass
class ListNews:
    name_source: str
    news: list[News]


def parse_list_news(raw_data: str) -> ListNews:
    """The program receives the necessary data about the latest news"""
    soup = BeautifulSoup(raw_data, 'xml')
    return ListNews(
        name_source=_parse_name_source(soup),
        news=_get_list_news(soup)
    )


def _get_list_news(soup: BeautifulSoup) -> list[News]:
    fresh_news = _get_last_news(soup)
    list_news = []
    for first_news in fresh_news:
        list_news.append(News(
            title=_parse_title(first_news),
            publication_time=_parse_time(first_news),
            description=_parse_description(first_news),
            link_news=_parse_link(first_news)))
    return list_news


def _parse_name_source(soup: BeautifulSoup) -> str:
    try:
        return soup.find('channel').title.text
    except AttributeError:
        raise CantGetNews


def _get_last_news(soup: BeautifulSoup) -> ResultSet:
    first_news = soup.find_all('item')[0:COUNT_NEWS]
    if not len(first_news):
        raise CantGetNews
    return first_news


def _parse_title(first_news: BeautifulSoup) -> str:
    try:
        return first_news.find('title').text
    except AttributeError:
        raise CantGetNews


def _parse_time(first_news: BeautifulSoup) -> datetime:
    dateFormatter = "%d %b %Y %H:%M:%S"
    try:
        dateString = str(' '.join(first_news.find('pubDate').text.split(' ')[1:5]))
    except AttributeError:
        raise CantGetNews
    try:
        return datetime.strptime(dateString, dateFormatter)
    except ValueError:
        raise CantGetNews


def _parse_description(first_news: BeautifulSoup) -> str:
    try:
        return first_news.find('description').text.strip()
    except AttributeError:
        raise CantGetNews


def _parse_link(first_news: BeautifulSoup) -> str:
    try:
        return first_news.find('link').text
    except AttributeError:
        raise CantGetNews

if __name__ == '__main__':
    from services.get_HTMl_or_RSS import get_html_page

    print(parse_list_news(get_html_page('https://lenta.ru/rss/top7')))
