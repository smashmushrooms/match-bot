import requests, bs4
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


class Score_Matches:
    '''
        example:
            score = Score_Matches()
            score.get_matches('Чемпионат Мира' , '2018-6-14')
            
    '''
    def __init__(self):
        pass

    def _check_date(self):
        if not isinstance(self._date, str):
            print('Date must be str')
            self._date = False
            return

        if len(self._date.split('-')) != 3:
            print('Incorrect date')
            self._date = False
            return

        year, month, day = np.array(self._date.split('-'), dtype=int)
        if year not in range(2018, 3000):
            print('Year in date must be from range(2018 , 3000)')
            self._date = False
            return

        if month not in range(1, 13):
            print('Month in date must be from range(1 , 13)')
            self._date = False
            return

        if day not in range(1, 31):
            print('Day in date must be from range(1 , 31)')
            self._date = False
            return

        self._date = str(year) + '-' + str(month) + '-' + str(day)

    def _get_url(self):

        if self._name_of_champ not in championats:
            print('Incorrect name of championat')
            self._url = False
            return

        _id = championats[self._name_of_champ]

        if not self._date:
            time = datetime.now()
            self._date = str(time.year) + '-' + \
                str(time.month) + '-' + str(time.day)
        else:
            self._check_date()
            if self._date == False:
                self._url = False
                return

        self._url = 'http://soccer365.ru/online/&competition_id=' + _id + '&date=' + self._date

    def _get_match_score(self):
        
        self._dict_match = {}
        
        if not self._url:
            return

        s = requests.get(self._url)
        b = bs4.BeautifulSoup(s.text, "html.parser")

        for i, match in enumerate(b.select('.game_block')):
            match = match.getText().replace('\t', '').replace('\xa0', '').split('\n')
            match = list(filter(lambda x: x != '', match))
            time = match[0]
            first_team = match[1][:-1]
            second_team = match[4]
            self._dict_match[i] = {'name_of_first': first_team, 'name_of_second': second_team,
                             'match': first_team + '-' + second_team,
                             'time': time, 'score_first': match[2], 'score_second': match[3]}

    def get_matches(self, name_of_champ, date=None):
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

        self._get_url()
        if self._url:
            self._get_match_score()
        return self._dict_match
