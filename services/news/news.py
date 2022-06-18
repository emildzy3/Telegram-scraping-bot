from exception import CantConnectToServer, CantGetNews
from services.get_HTMl_or_RSS import get_html_page
from services.news.parse_news import parse_list_news, ListNews, News
from settings import LIST_NEWS_SOURCE


def get_list_news() -> list[ListNews, News]:
    all_news = []
    for url in LIST_NEWS_SOURCE:
        try:
            raw_data = get_html_page(url)
        except CantConnectToServer:
            print('Не могу соединиться с сервером. Повторите попытку позже')
            exit(1)
        try:
            list_news = parse_list_news(raw_data)
        except CantGetNews:
            print('Не могу распарсить новости. Возможно введен неверный ключ')
            exit(1)
        all_news.append(list_news)
    return all_news


if __name__ == '__main__':
    print(get_list_news())
