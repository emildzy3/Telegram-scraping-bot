from dataclasses import dataclass
from bs4 import BeautifulSoup, ResultSet

from exception import CantGetCourse
from settings import COUNT_CRYPTO_COIN


@dataclass
class CryptoInfo:
    price: float
    changes_24_hours: str


@dataclass
class CryproCourse:
    name: str
    info: list[CryptoInfo]


def parse_crypto_course(data) -> list[CryproCourse]:
    soup = BeautifulSoup(data, 'lxml')
    return _get_course(soup)


def _get_course(soup: BeautifulSoup) -> list[CryproCourse]:
    trs = soup.find('table').find('tbody').find_all('tr')
    crypto_list = []
    for tr in trs[:COUNT_CRYPTO_COIN]:
        tds = tr.find_all('td')
        crypto_list.append(
            CryproCourse(
                name=_parse_name(tds),
                info=_parse_all_info(tds)
            )
        )
    return crypto_list


def _parse_name(tds: ResultSet) -> str:
    try:
        return tds[2].find('p').text
    except AttributeError:
        raise CantGetCourse

def _parse_all_info(tds: ResultSet) -> list[CryptoInfo]:
    list_inf_crypto = [CryptoInfo(
        price=_parse_price(tds),
        changes_24_hours=_parse_change(tds)
    )]
    return list_inf_crypto


def _parse_price(tds: ResultSet) -> float:
    try:
        return tds[3].find('a').text.split('$')[-1]
    except AttributeError:
        raise CantGetCourse

def _parse_change(tds: ResultSet) -> str:
    try:
        changes_24_hours_percent = tds[4].find('span').text
        changes_24_hours_up_or_down = tds[4].find('span').span['class'][0].split('-')[-1]
    except AttributeError:
        raise CantGetCourse
    return f'{changes_24_hours_up_or_down} {changes_24_hours_percent}'


if __name__ == '__main__':
    from services.get_HTMl_or_RSS import get_html_page
    from settings import URL_CRYPTO_EXCHANGE
    print(parse_crypto_course(get_html_page(URL_CRYPTO_EXCHANGE)))
