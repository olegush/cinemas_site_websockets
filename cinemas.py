import re

import asks
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from werkzeug.contrib.cache import FileSystemCache


TIMEOUT = 30
LIMITS = 3


async def get_content(url, payload, cache):
    """Fetch content from url or get it from cache."""
    cache = FileSystemCache(
        'cache',
        threshold=cache['threshold'],
        default_timeout=cache['default_timeout'],
        )
    cache_id = url + str(payload)
    cache_content = cache.get(cache_id)
    if cache_content is not None:
        return cache_content
    headers = {'user-agent': UserAgent().chrome}
    resp = await asks.get(
        url, params=payload, headers=headers, timeout=TIMEOUT, retries=LIMITS,
        )
    resp.raise_for_status()
    content = resp.text
    cache.set(cache_id, content)
    return content


def parse_afisha_page(html):
    """Afisha schedule page parser."""
    soup = BeautifulSoup(html, 'html.parser')
    movies = []

    for movie in soup.find_all('article', class_='films_item fav fav-film grid_cell3'):
        title = movie.find('span', class_='link_border').text
        descr_tag = movie.find('span', class_='films_info')
        genre = descr_tag.text
        year, country = descr_tag.next_element.next_element.next_element.text.split(',')#re.search(r'[\d+]{4}', descr).group(0)
        href = movie.find('a', class_='films_iconFrame')['href']
        id_afisha = re.search(r'\d+', href).group(0)
        movies.append(
            {'title': title, 'year': year, 'id_afisha': id_afisha, 'descr': f'{genre}, {country}'},
            )
    return movies


def parse_kinopoisk_page(html, year):
    """Kinopoisk movie page parser."""
    soup = BeautifulSoup(html, 'html.parser')
    try:
        for movie in soup.find_all('div', class_='element'):
            year_kp_tag = movie.find('span', class_='year')
            year_kp = int(year_kp_tag.string[:4])
            rating_tag = year_kp_tag.parent.parent.parent.find(
                'div', class_='rating',
                )
            rating_kp = float(rating_tag.string) if rating_tag else None
            if year_kp == year:
                title_eng_tag = movie.find(
                    'span', class_='gray',
                    ).text.rpartition(',')
                title_eng = title_eng_tag[0]
                runtime = title_eng_tag[2].strip()
                id_kinopoisk = year_kp_tag.parent.parent.find('a')['data-id']
                return {
                    'rating_kp': rating_kp,
                    'id_kinopoisk': id_kinopoisk,
                    'title_eng': title_eng,
                    'runtime':  runtime,
                    }
    except (TypeError, AttributeError):
        pass
    return {
        'rating_kp': None, 'id_kinopoisk': None, 'title_eng': '', 'runtime': '',
        }


def parse_imdb_page(html, year):
    """IMDB movie page parser."""
    soup = BeautifulSoup(html, 'html.parser')
    try:
        for movie in soup.find_all('div', class_='rating rating-list'):
            imdb = movie['id'].split('|')
            id_imdb = imdb[0]
            rating_imdb = imdb[2]
            return {'id_imdb': id_imdb, 'rating_imdb': float(rating_imdb)}
    except (TypeError, AttributeError):
        pass
    return {'id_imdb': '', 'rating_imdb': 0}
