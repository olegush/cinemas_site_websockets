import unittest

import requests
from fake_useragent import UserAgent

from cinemas import parse_afisha_page, parse_kinopoisk_page, parse_imdb_page


MOVIES_TEST = [{'title': 'Малефисента: Владычица тьмы', 'year': '2019', 'id_afisha': '8326540', 'descr': 'фэнтези, семейный, приключения,  США'}, {'title': 'Текст', 'year': '2019', 'id_afisha': '8355754', 'descr': 'драма,  Россия'}, {'title': 'Zомбилэнд: контрольный выстрел', 'year': '2019', 'id_afisha': '8329797', 'descr': 'комедия, ужасы,  США'}, {'title': 'Джокер', 'year': '2019', 'id_afisha': '8354928', 'descr': 'криминал, драма,  США'}, {'title': 'Эверест', 'year': '2019', 'id_afisha': '8329045', 'descr': 'анимация,  США'}, {'title': 'Урфин Джюс возвращается', 'year': '2019', 'id_afisha': '8329886', 'descr': 'анимация,  Россия'}, {'title': 'Сельма в городе призраков', 'year': '2019', 'id_afisha': '8355956', 'descr': 'анимация, приключения,  Мексика'}, {'title': 'Три секунды', 'year': '2018', 'id_afisha': '8353708', 'descr': 'криминал, драма,  Великобритания'}, {'title': 'Гемини', 'year': '2019', 'id_afisha': '8330487', 'descr': 'боевик, драма, фантастика,  США'}, {'title': 'Дождливый день в Нью-Йорке', 'year': '2018', 'id_afisha': '8354419', 'descr': 'драма,  США'}, {'title': 'Поменяться местами', 'year': '2019', 'id_afisha': '8355430', 'descr': 'мелодрама, комедия,  Франция'}, {'title': 'Арахисовый сокол', 'year': '2019', 'id_afisha': '8356249', 'descr': 'приключения,  США'}, {'title': 'Окей, Лекси!', 'year': '2019', 'id_afisha': '8356526', 'descr': 'комедия,  США'}, {'title': 'Дикая лига', 'year': '2019', 'id_afisha': '8330125', 'descr': 'спорт, исторический, драма,  Россия'}, {'title': 'Матрица', 'year': '1999', 'id_afisha': '3788758', 'descr': 'боевик, фантастика, триллер,  Австралия / США'}, {'title': 'Иные', 'year': '2018', 'id_afisha': '8356055', 'descr': 'фантастика, триллер, драма,  США / Канада'}, {'title': 'Они', 'year': '2019', 'id_afisha': '8356360', 'descr': 'ужасы,  США'}, {'title': 'Сторож', 'year': '2018', 'id_afisha': '8330332', 'descr': 'драма,  Россия'}, {'title': 'Щенячий патруль: Мегащенки и Шиммер и Шайн', 'year': '2019', 'id_afisha': '8356463', 'descr': 'анимация, детский,  США / Канада'}, {'title': 'Портрет девушки в огне', 'year': '2019', 'id_afisha': '8356076', 'descr': 'драма, исторический,  Франция'}, {'title': 'Побег из Шоушенка', 'year': '1994', 'id_afisha': '7731571', 'descr': 'драма, триллер,  США'}, {'title': 'Кокаиновый барон', 'year': '2018', 'id_afisha': '8355407', 'descr': 'триллер, криминал, боевик,  США / Колумбия'}, {'title': 'Троица', 'year': '2019', 'id_afisha': '8356186', 'descr': 'драма, мелодрама,  Россия'}, {'title': 'К звездам', 'year': '2018', 'id_afisha': '8329226', 'descr': 'фантастика, драма,  США / Бразилия'}, {'title': 'Джуди', 'year': '2019', 'id_afisha': '8354463', 'descr': 'музыкальный, биография,  Великобритания'}, {'title': 'Девушки бывают разные', 'year': '2019', 'id_afisha': '8356462', 'descr': 'комедия,  Россия'}, {'title': 'Прощание', 'year': '2019', 'id_afisha': '8356229', 'descr': 'комедия, драма,  США'}, {'title': 'Мысленный волк', 'year': '2019', 'id_afisha': '8330135', 'descr': 'драма, мистика,  Россия'}, {'title': 'Однажды в... Голливуде', 'year': '2019', 'id_afisha': '8354335', 'descr': 'комедия, драма,  США'}, {'title': 'МУЛЬТ в кино. Выпуск 105. Зима близко!', 'year': '2019', 'id_afisha': '8356648', 'descr': 'анимация, детский, семейный,  Россия'}, {'title': 'Тайна печати дракона', 'year': '2019', 'id_afisha': '8171095', 'descr': 'приключения, фэнтези,  Россия / Китай'}, {'title': 'Королевские каникулы', 'year': '2018', 'id_afisha': '8356119', 'descr': 'анимация,  Канада / США'}, {'title': 'Raving Riot: Рейв у парламента', 'year': '2019', 'id_afisha': '8356570', 'descr': 'документальный,  Грузия / Россия'}, {'title': 'Терминатор 2: Судный день 3D', 'year': '2017', 'id_afisha': '8327702', 'descr': 'боевик, триллер,  США'}, {'title': 'Паразиты', 'year': '2019', 'id_afisha': '8355519', 'descr': 'драма, триллер,  Корея'}, {'title': 'Зеленее травы', 'year': '2019', 'id_afisha': '8355796', 'descr': 'комедия,  США'}, {'title': 'Рэмбо: Последняя кровь', 'year': '2019', 'id_afisha': '7831985', 'descr': 'боевик, триллер,  США'}, {'title': 'Король Лев', 'year': '2019', 'id_afisha': '8329617', 'descr': 'фантастика, семейный,  США'}, {'title': 'Люби их всех', 'year': '2018', 'id_afisha': '8330295', 'descr': 'драма, триллер,  Россия'}, {'title': 'Щегол', 'year': '2019', 'id_afisha': '8353770', 'descr': 'драма,  США'}, {'title': 'Зеленая книга', 'year': '2018', 'id_afisha': '8355131', 'descr': 'драма,  США'}, {'title': 'Акварель', 'year': '2018', 'id_afisha': '8355253', 'descr': 'документальный,  Великобритания / Дания'}, {'title': 'Работа без авторства', 'year': '2018', 'id_afisha': '8355726', 'descr': 'триллер, драма, мелодрама,  Германия / Италия'}, {'title': 'Я вернусь', 'year': '2018', 'id_afisha': '8356550', 'descr': 'драма,  Россия / Армения'}, {'title': 'Андрей Тарковский. Кино как молитва', 'year': '2019', 'id_afisha': '8356620', 'descr': 'документальный,  Россия / Италия / Швеция'}, {'title': 'Интимный дневник Анны Карениной', 'year': '2017', 'id_afisha': '8323010', 'descr': 'драма,  Россия'}, {'title': 'Идеальные незнакомцы', 'year': '2016', 'id_afisha': '8328292', 'descr': 'драма, комедия,  Италия'}, {'title': 'Angry Birds 2 в кино', 'year': '2019', 'id_afisha': '8329714', 'descr': 'анимация, детский,  США'}, {'title': 'Игры разумов', 'year': '2018', 'id_afisha': '8329936', 'descr': 'драма, детектив, биография,  Ирландия'}, {'title': 'Подкидыш', 'year': '2019', 'id_afisha': '8330147', 'descr': 'драма, комедия,  Россия'}, {'title': 'Оно 2', 'year': '2019', 'id_afisha': '8331033', 'descr': 'ужасы, триллер,  США'}, {'title': 'Хокусай', 'year': '2017', 'id_afisha': '8354110', 'descr': 'документальный,  Великобритания / Япония / США'}, {'title': 'Yesterday', 'year': '2019', 'id_afisha': '8354726', 'descr': 'музыкальный, комедия,  Великобритания'}, {'title': 'Романтики 303', 'year': '2018', 'id_afisha': '8355040', 'descr': 'комедия, мелодрама,  Германия'}, {'title': 'Приключения Реми', 'year': '2019', 'id_afisha': '8355057', 'descr': 'драма,  Франция'}, {'title': 'Страшные истории для рассказа в темноте', 'year': '2019', 'id_afisha': '8355402', 'descr': 'ужасы,  США'}, {'title': 'Добыча', 'year': '2018', 'id_afisha': '8355426', 'descr': 'ужасы, триллер,  США'}, {'title': 'Варда глазами Аньес', 'year': '2019', 'id_afisha': '8355643', 'descr': 'документальный,  Франция'}, {'title': 'Соблазн', 'year': '2019', 'id_afisha': '8355832', 'descr': 'триллер, драма,  Франция'}, {'title': 'Стриптизерши', 'year': '2019', 'id_afisha': '8356054', 'descr': 'триллер, драма,  США'}, {'title': 'Собаки не носят штанов', 'year': '2019', 'id_afisha': '8356145', 'descr': 'драма,  Финляндия / Латвия'}, {'title': 'Промар', 'year': '2019', 'id_afisha': '8356241', 'descr': 'аниме ,  Япония'}, {'title': 'Короли интриги', 'year': '2019', 'id_afisha': '8356273', 'descr': 'детектив, комедия,  Аргентина / Испания'}, {'title': 'TheatreHD: Фаэтон', 'year': '2019', 'id_afisha': '8356343', 'descr': 'опера,  Россия'}, {'title': 'Кокоша — маленький дракон: Приключения в джунглях', 'year': '2018', 'id_afisha': '8356361', 'descr': 'анимация, семейный,  Германия'}, {'title': 'Братья Медведи: Тайна трех миров', 'year': '2018', 'id_afisha': '8356362', 'descr': 'анимация, детский,  Китай'}, {'title': 'Петсон и Финдус. Финдус переезжает', 'year': '2018', 'id_afisha': '8356372', 'descr': 'анимация, семейный,  Германия'}, {'title': 'Музей Прадо: Коллекция чудес', 'year': '2019', 'id_afisha': '8356375', 'descr': 'документальный,  Испания'}, {'title': 'Симфония природы', 'year': '2019', 'id_afisha': '8356592', 'descr': 'документальный, музыкальный,  Финляндия'}]


MOVIE_KP_TEST = {'rating_kp': 7.1, 'id_kinopoisk': '916498', 'title_eng': 'Maleficent: Mistress of Evil', 'runtime': '118 мин'}

MOVIE_IMDB_TEST = {'id_imdb': 'tt4777008', 'rating_imdb': 7.1}


class TestParsing(unittest.TestCase):
    """Parsing functions tests."""

    def test_status_code_afisha_page(self):
        headers = {'user-agent': UserAgent().chrome}
        params = {'view': 'list'}
        resp = requests.get('https://spb.kinoafisha.info/movies/', params=params, headers=headers)
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
        year = int(MOVIES_TEST[0]['year'])
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
