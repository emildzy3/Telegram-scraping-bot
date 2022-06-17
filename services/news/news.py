from services.news.get_news_RSS import get_html_page
from services.news.parse_news import parse_list_news
from settings import LIST_NEWS_SOURCE


def get_list_news() -> str:
    for url in LIST_NEWS_SOURCE:
        raw_data = get_html_page(url)
        list_news = parse_list_news(raw_data)
        # return print_list_news(list_news)


if __name__ == '__main__':
    get_list_news()
