from dataclasses import dataclass
from datetime import datetime
from typing import Union

from bs4 import BeautifulSoup, ResultSet

from settings import COUNT_NEWS

Url = str


@dataclass
class News:
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


def _get_list_news(soup: Union[BeautifulSoup, BeautifulSoup]) -> list[News]:
    fresh_news = _get_last_news(soup)
    list_news = []
    for news in fresh_news:
        list_news.append(News(
            publication_time=_parse_time(news),
            description=_parse_description(news),
            link_news=_parse_link(news)))
    return list_news


def _get_last_news(soup: Union[BeautifulSoup, BeautifulSoup]) -> ResultSet:
    first_three_news = soup.find_all('item')[0:COUNT_NEWS]
    return first_three_news


def _parse_name_source(soup: Union[BeautifulSoup, BeautifulSoup]) -> str:
    source_name = soup.find('channel').title.text
    return source_name


def _parse_time(first_three_news: Union[BeautifulSoup, BeautifulSoup]) -> datetime:
    dateString = str(' '.join(first_three_news.find('pubDate').text.split(' ')[1:5]))
    dateFormatter = "%d %b %Y %H:%M:%S"
    return datetime.strptime(dateString, dateFormatter)


def _parse_description(first_three_news: Union[BeautifulSoup, BeautifulSoup]) -> str:
    return first_three_news.find('description').text.strip()


def _parse_link(first_three_news: Union[BeautifulSoup, BeautifulSoup]) -> str:
    return first_three_news.find('link').text


if __name__ == '__main__':
    pass
