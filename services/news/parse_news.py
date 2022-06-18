from dataclasses import dataclass
from datetime import datetime

from bs4 import BeautifulSoup, ResultSet, PageElement

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
    source_name = soup.find('channel').title.text
    return source_name


def _get_last_news(soup: BeautifulSoup) -> ResultSet:
    first_news = soup.find_all('item')[0:COUNT_NEWS]
    return first_news


def _parse_title(first_news: BeautifulSoup) -> str:
    title = first_news.find('title').text
    return title


def _parse_time(first_news: BeautifulSoup) -> datetime:
    dateString = str(' '.join(first_news.find('pubDate').text.split(' ')[1:5]))
    dateFormatter = "%d %b %Y %H:%M:%S"
    return datetime.strptime(dateString, dateFormatter)


def _parse_description(first_news: BeautifulSoup) -> str:
    return first_news.find('description').text.strip()


def _parse_link(first_news: BeautifulSoup) -> str:
    return first_news.find('link').text


if __name__ == '__main__':
    from services.news.get_news_RSS import get_html_page

    print(parse_list_news(get_html_page('https://lenta.ru/rss/top7')))
