URL = 'http://api-hack.photolab.me/template_process.php'

templates_names = {
    'versus': '10B527DA-8896-8304-018D-2C24F5492476',
    'soccer_man': '4283E3C4-BE89-42A4-D9B5-B775A66F146F'
}

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
                   'Япония': 'Russia'
                   }

english2russian = dict(zip(russian2english.values(), russian2english.keys()))


country_flag = {"Russia": 'http://www.world-globe.ru/files/flags/russia_l.png',
                'Saudi Arabia': 'http://www.world-globe.ru/files/flags/saudi-arabia_l.png',
                'Portugal': 'http://www.world-globe.ru/files/flags/portugal_l.png',
                'Spain': 'http://www.world-globe.ru/files/flags/spain_l.png',
                'Morocco': 'http://www.world-globe.ru/countries/morocco/flag/',
                'IR Iran': 'http://www.world-globe.ru/files/flags/iran_l.png',
                'Egypt': 'http://www.world-globe.ru/files/flags/egypt_l.png',
                'Uruguay': 'http://www.world-globe.ru/files/flags/uruguay_l.png',
                'Croatia': 'http://www.world-globe.ru/files/flags/croatia_l.png',
                'Nigeria': 'http://www.world-globe.ru/files/flags/nigeria_l.png',
                'Peru': 'http://www.world-globe.ru/files/flags/peru_l.png',
                'Denmark': 'http://www.world-globe.ru/files/flags/denmark_l.png',
                'Argentina': 'http://www.world-globe.ru/files/flags/argentina_l.png',
                'Iceland': 'http://www.world-globe.ru/files/flags/iceland_l.png',
                'France': 'http://www.world-globe.ru/files/flags/france_l.png',
                'Australia': 'http://www.world-globe.ru/files/flags/australia_l.png',
                'Brazil': 'http://www.world-globe.ru/files/flags/brazil_l.png',
                'Switzerland': 'http://www.world-globe.ru/files/flags/switzerland_l.png',
                'Germany': 'http://www.world-globe.ru/files/flags/germany_l.png',
                'Mexico': 'http://www.world-globe.ru/files/flags/mexico_l.png',
                'Costa Rica': 'http://www.world-globe.ru/files/flags/costa-rica_l.png',
                'Serbia': 'http://www.world-globe.ru/files/flags/serbia_l.png',
                'Tunisia': 'http://www.world-globe.ru/files/flags/tunisia_l.png',
                'England': 'http://www.clipartbest.com/cliparts/RcG/ErL/RcGErLG4i.jpg',
                'Belgium': 'http://www.world-globe.ru/files/flags/belgium_l.png',
                'Panama': 'http://www.world-globe.ru/files/flags/panama_l.png',
                'Sweden': 'http://www.world-globe.ru/files/flags/sweden_l.png',
                'Korea Republic': 'http://www.world-globe.ru/files/flags/south-korea_l.png',
                'Poland': 'http://www.world-globe.ru/files/flags/poland_l.png',
                'Senegal': 'http://www.world-globe.ru/files/flags/senegal_l.png',
                'Colombia': 'http://www.world-globe.ru/files/flags/colombia_l.png',
                'Russia': 'http://www.world-globe.ru/files/flags/Russia_l.png'
                }

city2stadium = {   'Москва': 'https://spartakfanat.ru/gallery/stadion/Otkrytie_Arena_18.jpg',
                   'Санкт-Петербург': 'http://liport.ru/uploads/posts/2018-01/igor-albin-stadion-sankt-peterburg-budet-peredan-vkoncessiyu-zenitu_1.jpg',
                   'Калининград': 'https://worldcap2018.ru/wp-content/uploads/2017/02/Vid-na-pole-1.jpg',
                   'Волгоград': 'https://pbs.twimg.com/media/DUOcZTsXcAAzNM5.jpg',
                   'Екатеринбург': 'https://media.nakanune.ru/images/pictures/image_big_127972.jpg',
                   'Казань': 'http://stadiums.at.ua/_nw/306/14515256.jpg',
                   'Нижний Новгород': 'https://eventticketmaster.com/image/stadiums/stadion-nizhny-novgorod.jpg',
                   'Ростов-на-Дону': 'http://rostov-arena.ml/wp-content/uploads/2017/10/rostov-arena-vid-nochyu.jpg',
                   'Самара': 'http://progorodsamara.ru/userfiles/picoriginal/img-20160315175656-159.jpg',
                   'Саранск': 'https://rg.ru/i/gallery/98c3b2fa/1_506cea07.jpg',
                   'Сочи': 'https://tropki.ru/sites/default/files/styles/article/public/previews/17127/stadion-fisht_0.jpg?itok=eKqyPXlR'
           }
