import unittest

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from cinemas import get_content, parse_afisha_page, parse_kinopoisk_page, parse_imdb_page


MOVIES_TEST = [{'title': 'Малефисента: Владычица тьмы', 'year': 2019, 'id_afisha': '246869', 'descr': 'Лесная ведьма убеждена: свадьбы не будет!'}, {'title': 'Джокер', 'year': 2019, 'id_afisha': '244777', 'descr': 'Хоакин Феникс в серьезной драме про безумного шута Готэма'}, {'title': 'Окей, Лекси!', 'year': 2019, 'id_afisha': '257864', 'descr': 'Безбашенная комедия про взбесившийся виртуальный разум'}, {'title': 'Дождливый день в Нью-Йорке', 'year': 2019, 'id_afisha': '246304', 'descr': 'Акварельная зарисовка Вуди Аллена в родном городе'}, {'title': 'Эверест', 'year': 2019, 'id_afisha': '230687', 'descr': 'Йети и девочка взбираются на горный пик'}, {'title': 'Прощание', 'year': 2019, 'id_afisha': '257360', 'descr': 'Хит «Сандэнса», уютная трагикомедия о чрезмерной заботе'}, {'title': 'Гемини', 'year': 2019, 'id_afisha': '231970', 'descr': 'Новаторская фантастика от режиссера «Крадущегося тигра, затаившегося дракона», «Халка» и «Горбатой горы»'}, {'title': 'Они', 'year': 2019, 'id_afisha': '257501', 'descr': 'Хоррор на Хеллоуин про комнаты ужаса'}, {'title': 'Девушки бывают разные', 'year': 2019, 'id_afisha': '257610', 'descr': 'Летняя разнузданная комедия с переодеваниями'}, {'title': 'Джуди', 'year': 2018, 'id_afisha': '244496', 'descr': 'Потенциальный «Оскар» в руках Рене Зеллвегер'}, {'title': 'Мысленный волк', 'year': 2019, 'id_afisha': '257237', 'descr': 'Околоправославный хоррор Валерии Гай Германики с Юлией Высоцкой и Елизаветой Климовой'}, {'title': 'Зеленее травы', 'year': 2019, 'id_afisha': '257028', 'descr': 'Абсурдистская комедия из жизни пригорода'}, {'title': 'Тайна печати дракона', 'year': 2019, 'id_afisha': '224918', 'descr': 'Российско-китайское фэнтези с Джеки Чаном и Арнольдом Шварценеггером'}, {'title': 'Оно-2', 'year': 2019, 'id_afisha': '232938', 'descr': 'Просто дети стали старше: сиквел самого прибыльного хоррора в истории (и по Кингу)'}, {'title': 'Однажды... в Голливуде', 'year': 2019, 'id_afisha': '246118', 'descr': 'Девятый фильм Квентина Тарантино про омытую кровью «фабрику грез»'}, {'title': 'К звездам', 'year': 2019, 'id_afisha': '233024', 'descr': 'Брэд Питт отправляется в космос в новом фильме Джеймса Грея'}, {'title': 'Паразиты', 'year': 2019, 'id_afisha': '246915', 'descr': 'Одна семья пытается завладеть состоянием другой с помощью нетривиальных методов: новый фильм именитого корейца Пона Чжун Хо'}, {'title': 'Соблазн', 'year': 2019, 'id_afisha': '246413', 'descr': 'Психологическая драма о двух женщинах'}, {'title': 'Волшебник', 'year': 2019, 'id_afisha': '244674', 'descr': 'Семен Трескунов учится быть рок-н-ролльщиком у Максима Суханова'}, {'title': 'Дети моря', 'year': 2019, 'id_afisha': '257706', 'descr': 'Аниме про девочку и ее морских друзей'}, {'title': 'Короли интриги', 'year': 2019, 'id_afisha': '257332', 'descr': 'Залихватский детектив от обладателя премии «Оскар»'}, {'title': 'Последнее испытание', 'year': 2018, 'id_afisha': '243847', 'descr': 'Сиквел «Училки» с захватом заложников'}, {'title': 'Герой', 'year': 2019, 'id_afisha': '245262', 'descr': 'Отечественный шпионский триллер с Александром Петровым и Владимиром Машковым'}, {'title': 'Игра с огнем', 'year': 2019, 'id_afisha': '246791', 'descr': 'Триллер, вдохновленный «Фарго» братьев Коэнов'}]

MOVIE_KP_TEST = {'rating_kp': 7.1, 'id_kinopoisk': '916498', 'title_eng': 'Maleficent: Mistress of Evil', 'runtime': '118 мин'}

MOVIE_IMDB_TEST = {'id_imdb': 'tt4777008', 'rating_imdb': 7.1}


class TestParsing(unittest.TestCase):
    """Parsing functions tests."""

    def test_status_code_afisha_page(self):
        headers = {'user-agent': UserAgent().chrome}
        params = {'view': 'list'}
        resp = requests.get('https://www.afisha.ru/spb/schedule_cinema/', params=params, headers=headers)
        self.assertEqual(resp.status_code, 200)

    def test_parse_afisha_page(self):
        with open('test_afisha.html', encoding='utf-8') as file:
            html = file.read()
        movies = parse_afisha_page(html)
        self.assertEqual(movies, MOVIES_TEST)

    def test_status_code_kinopoisk_page(self):
        headers = {'user-agent': UserAgent().chrome}
        title = MOVIES_TEST[0]['title']
        year = MOVIES_TEST[0]['year']
        params = {'kp_query': f'{title} {year}'}
        resp = requests.get('https://www.kinopoisk.ru/index.php', params=params, headers=headers)
        self.assertEqual(resp.status_code, 200)

    def test_parse_kinopoisk_page(self):
        year = MOVIES_TEST[0]['year']
        with open('test_kinopoisk.html', encoding='utf-8') as file:
            html = file.read()
        movie = parse_kinopoisk_page(html, year)
        self.assertEqual(movie, MOVIE_KP_TEST)

    def test_status_code_imdb_page(self):
        headers = {'user-agent': UserAgent().chrome}
        title = MOVIE_KP_TEST['title_eng']
        year = MOVIES_TEST[0]['year']
        params = {
            'title': title,
            'title_type': 'feature',
            'release_date': f'{year},{year}',
            }
        resp = requests.get('https://www.imdb.com/search/title/', params=params, headers=headers)
        self.assertEqual(resp.status_code, 200)

    def test_parse_imdb_page(self):
        year = MOVIES_TEST[0]['year']
        with open('test_imdb.html', encoding='utf-8') as file:
            html = file.read()
        movie = parse_imdb_page(html, year)
        self.assertEqual(movie, MOVIE_IMDB_TEST)


if __name__ == '__main__':
    unittest.main()
