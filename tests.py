import unittest

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from cinemas import get_content, parse_afisha_page, parse_kinopoisk_page, parse_imdb_page


class TestParsing(unittest.TestCase):
    """Parsing functions tests."""

    def setUp(self):
        headers = {'user-agent': UserAgent().chrome}
        params = {'view': 'list'}
        self.resp = requests.get('https://www.afisha.ru/spb/schedule_cinema/', params=params, headers=headers)

    def test_status_code_afisha_page(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_parse_afisha_page(self):
        html = self.resp.text
        soup = BeautifulSoup(html, 'html.parser')
        movies = soup.find_all('div', class_='new-list__item movie-item')
        self.assertTrue(len(movies) > 0)
        for movie in movies:
            title = movie.find('a', class_='new-list__item-link')
            self.assertTrue(title is not None)

if __name__ == '__main__':
    unittest.main()
