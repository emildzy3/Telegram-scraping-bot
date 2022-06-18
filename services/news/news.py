from services.info_formatter import print_news
from services.news.get_news_RSS import get_html_page
from services.news.parse_news import parse_list_news, ListNews, News
from settings import LIST_NEWS_SOURCE, COUNT_NEWS


def get_list_news() -> list[ListNews, News]:
    all_news = []
    for url in LIST_NEWS_SOURCE:
        raw_data = get_html_page(url)
        list_news = parse_list_news(raw_data)
        all_news.append(list_news)
    return all_news


if __name__ == '__main__':
    print(get_list_news())
