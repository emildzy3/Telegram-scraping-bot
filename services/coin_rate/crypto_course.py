from exception import CantConnectToServer, CantGetCourse
from services.coin_rate.parse_crypto import parse_crypto_course, CryproCourse
from services.get_HTMl_or_RSS import get_html_page
from settings import URL_CRYPTO_EXCHANGE


def get_crypto_course() -> list[CryproCourse]:
    try:
        raw_data = get_html_page(URL_CRYPTO_EXCHANGE)
    except CantConnectToServer:
        print('Не могу соединиться с сервером. Повторите попытку позже')
        exit(1)
    try:
        return parse_crypto_course(raw_data)
    except CantGetCourse:
        print(f'Не могу распарсить данные с сайта {URL_CRYPTO_EXCHANGE}. Возможно введен неверный ключ')
        exit(1)



if __name__ == '__main__':
    print(get_crypto_course())
