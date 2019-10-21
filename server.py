import json

import trio
from trio_websocket import serve_websocket, ConnectionClosed, ConnectionRejected
from asks.errors import BadStatus, RequestTimeout

from cinemas import get_content, parse_afisha_page, parse_kinopoisk_page, parse_imdb_page


SERVER = '127.0.0.1'
PORT = 8080
URL_AFISHA = 'https://www.afisha.ru/spb/schedule_cinema/'
CACHE_AFISHA = {'threshold': 1, 'default_timeout': 60*60*1}
URL_KP = 'https://www.kinopoisk.ru/index.php'
CACHE_KP = {'threshold': 100, 'default_timeout': 60*60*24}
URL_IMDB = 'https://www.imdb.com/search/title/'
CACHE_IMDB = {'threshold': 100, 'default_timeout': 60*60*24}
MOVIES_COUNT = 24
DELAY = 0.5


async def handle_movie(ws, movie):
    """Handler-function sends fetch and parsing results to socket."""
    payload_kp = {'kp_query': '{0} {1}'.format(movie['title'], movie['year'])}
    content_kp = await get_content(URL_KP, payload_kp, CACHE_KP)
    kp_movie = parse_kinopoisk_page(content_kp, movie['year'])
    if kp_movie['id_kinopoisk']:
        if kp_movie['title_eng'] == '':
            kp_movie['imdb'] = ''
            kp_movie['rating_imdb'] = 0
        else:
            year = movie['year']
            payload_imdb = {
                'title': kp_movie['title_eng'],
                'title_type': 'feature',
                'release_date': f'{year},{year}',
                }
            content_imdb = await get_content(URL_IMDB, payload_imdb, CACHE_IMDB)
            kp_movie.update(parse_imdb_page(content_imdb, movie['year']))
        movie.update(kp_movie)
        await ws.send_message(json.dumps(movie))


async def handle_server(request):
    """Trio nursery for handler-functions."""
    movies = []
    ws = await request.accept()
    payload_afisha = {'view': 'list'}
    content_afisha = await get_content(URL_AFISHA, payload_afisha, CACHE_AFISHA)
    movies = parse_afisha_page(content_afisha)
    try:
        async with trio.open_nursery() as nursery:
            for movie in movies:
                await trio.sleep(DELAY)
                nursery.start_soon(handle_movie, ws, movie)
    except ConnectionClosed:
        pass
    except ConnectionRejected:
        pass
    except BadStatus:
        pass
    except RequestTimeout:
        pass
    await ws.send_message('completed')


async def main():
    """Serve a WebSocket over TCP."""
    await serve_websocket(handle_server, SERVER, PORT, ssl_context=None)


trio.run(main)
