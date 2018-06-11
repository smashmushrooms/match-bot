import requests
import bs4
import numpy as np
from datetime import datetime

championats = {'Англия, Премьер лига': '12',
               'Россия, Премьер лига': '13',
               'Украина, Премьер лига': '14',
               'Италия, Серия А': '15',
               'Испания, Примера': '16',
               'Германия, Бундеслига': '17',
               'Франция, Лига 1': '18',
               'Лига Чемпионов': '19',
               'Лига Европы': '20',
               'Чемпионат Европы': '24',
               'Чемпионат Мира': '742'
               }

russian2english = {'Россия': 'Russia',
                   'Саудовская Аравия': 'Saudi Arabia',
                   'Португалия': 'Portugal',
                   'Испания': 'Spain',
                   'Марокко': 'Morocco',
                   'Иран': 'IR Iran',
                   'Египет': 'Egypt',
                   'Уругвай': 'Uruguay',
                   'Хорватия': 'Croatia',
                   'Нигерия': 'Nigeria',
                   'Перу': 'Peru',
                   'Дания': 'Denmark',
                   'Аргентина': 'Argentina',
                   'Исландия': 'Iceland',
                   'Франция': 'France',
                   'Австралия': 'Australia',
                   'Бразилия': 'Brazil',
                   'Швейцария': 'Switzerland',
                   'Германия': 'Germany',
                   'Мексика': 'Mexico',
                   'Коста-Рика': 'Costa Rica',
                   'Сербия': 'Serbia',
                   'Тунис': 'Tunisia',
                   'Англия': 'England',
                   'Бельгия': 'Belgium',
                   'Панама': 'Panama',
                   'Швеция': 'Sweden',
                   'Южная Корея': 'Korea Republic',
                   'Польша': 'Poland',
                   'Сенегал': 'Senegal',
                   'Колумбия': 'Colombia',
                   'Япония': 'Japan'
                   }


class Score_Matches:
    '''
        example:
            score = Score_Matches('Чемпионат Мира' , '2018-6-19')
            score.get_matches_names()
            >>>[['Russia', 'Egypt'], ['Poland', 'Senegal'], ['Colombia', 'Japan']]

            score.get_score(['Poland', 'Senegal'])
            >>>{'score_first': '-',
                'score_second': '-',
                'time': datetime.datetime(2018, 6, 19, 18, 0)}

    '''

    def __init__(self, name_of_champ='Чемпионат Мира', date=None):
        '''
            name_of_champ - str:
                Supported Championships:
                    'Чемпионат Мира',
                    'Чемпионат Европы',
                    'Англия, Премьер лига',
                    'Россия, Премьер лига',
                    'Украина, Премьер лига',
                    'Италия, Серия А',
                    'Испания, Примера',
                    'Германия, Бундеслига',
                    'Франция, Лига 1',
                    'Лига Чемпионов',
                    'Лига Европы'

            date - str:
                format - year-month-day
        '''
        self._name_of_champ = name_of_champ
        self._date = date

        self._dict_match = {}
        self._url = False

        self._get_matches()

    def _check_date(self):
        '''
            Date check.
        '''
        if not isinstance(self._date, str):
            print('Date must be str')
            self._date = False
            return

        if len(self._date.split('-')) != 3:
            print('Incorrect date format')
            self._date = False
            return

        year, month, day = np.array(self._date.split('-'), dtype=int)

        try:
            datetime(year, month, day)
        except Exception as error:
            print(error)
            self._date = False
            return

        self._date = str(year) + '-' + str(month) + '-' + str(day)

    def _get_url(self):
        '''
            Generation of the request url.
        '''

        if self._name_of_champ not in championats:
            print('Incorrect name of championat')
            return

        _id = championats[self._name_of_champ]

        if not self._date:
            time = datetime.now()
            self._date = str(time.year) + '-' + \
                str(time.month) + '-' + str(time.day)
        else:
            self._check_date()
            if self._date == False:
                return

        self._url = 'http://soccer365.ru/online/&competition_id=' + \
            _id + '&date=' + self._date

    def _get_match_score(self):
        '''
            Getting information about matches by url.
        '''
        if not self._url:
            return

        s = requests.get(self._url)
        b = bs4.BeautifulSoup(s.text, "html.parser")

        for match in b.select('.game_block'):
            match = match.getText().replace('\t', '').replace('\xa0', '').split('\n')
            match = list(filter(lambda x: x != '', match))

            time = match[0].replace(' ', '').replace("'", '').split(',')[-1]

            if self._name_of_champ == 'Чемпионат Мира':
                try:
                    first_team = russian2english[match[1][:-1]]
                    second_team = russian2english[match[4]]
                except:
                    print('Team has not yet been determined')
                    return
            else:
                first_team = match[1][:-1]
                second_team = match[4]
            score_first = match[2]
            score_second = match[3]
            match_name = first_team + '__' + second_team

            self._dict_match[match_name] = {'first_team': first_team,
                                            'second_team': second_team,
                                            'time': time,
                                            'score_first': score_first,
                                            'score_second': score_second}

    def _get_matches(self):
        '''
            Processing of all necessary functions.
        '''
        self._get_url()
        if self._url:
            self._get_match_score()
        return self._dict_match

    def get_matches_names(self):
        '''
            Getting a list of all matches on the date.
        '''
        self._names = list(self._dict_match.keys())
        return [i.split('__') for i in self._names]

    def get_score(self, teams):
        '''
            teams - list:
                format - [first_team , second_team]
                first_team - str
                second_team - str
        '''
        match_name = '__'.join(teams)
        if match_name not in self._names:
            print('This match is not today')
            return {}
        match = self._dict_match[match_name]
        return {'time': match['time'], 'score_first': match['score_first'], 'score_second': match['score_second']}
