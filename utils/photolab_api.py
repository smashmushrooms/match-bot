import requests
import bs4
import numpy as np
from utils.used_dict import *


def post2photlab_versus(photos, teams):
    """
        Generate versus photo
        photos - list of url as type str
        teams - list of url teams flags as type str

        example:
            url1 = 'http://www.wallpapersin4k.org/wp-content/uploads/2016/12/Man-Wallpapers-3.jpg'
            url2 = 'http://games-of-thrones.ru/sites/default/files/pictures/all/Ben%20Affleck/28.jpg'
            print(post2photlab_versus([url1, url2], ['Brazil', 'Germany']))
    """
    if not isinstance(photos, list):
        print('photos must be list')
        return ''

    if not isinstance(teams, list):
        print('teams must be list')
        return ''

    if len(photos) != 2:
        print('len photos must be equal 2')
        return ''

    if len(teams) != 2:
        print('len teams must be equal 2')
        return ''

    if not isinstance(photos[0], str) or not isinstance(photos[1], str):
        print('each element of photos must be str')
        return ''

    if not isinstance(teams[0], str) or not isinstance(teams[1], str):
        print('each element of teams must be str')
        return ''

    if teams[0] not in country_flag:
        print('unknown country ' + teams[0])
        return ''

    if teams[1] not in country_flag:
        print('unknown country ' + teams[1])
        return ''

    url1 = photos[0]
    url2 = photos[1]
    url3 = country_flag[teams[0]]
    url4 = country_flag[teams[1]]

    files = {'image_url[1]': (None, url1),
             'image_url[2]': (None, url2),
             'image_url[3]': (None, url3),
             'image_url[4]': (None, url4),
             'template_name': (None, templates_names['versus'])}

    response = requests.post(URL, files=files)

    return response.text


def post2photlab_stadium(photo, country, city):
    """
        Generate photo by template
        photos - url - str
        country - name of country in english - str
        city - name of city in russian (use get_city from score_matches)
        example:
            url = 'http://www.wallpapersin4k.org/wp-content/uploads/2016/12/Man-Wallpapers-3.jpg'
            country = 'England'
            city = 'Москва'
            print(post2photlab_stadium(url, country , city))
    """
    if not isinstance(photo, str):
        print('photos must be str')
        return ''

    if not isinstance(country, str):
        print('country must be str')
        return ''

    if not isinstance(city, str):
        print('stadium must be str')
        return ''

    if country not in country_flag:
        print('unknown name of country')
        return ''

    if city not in city2stadium:
        print('unknown name of city')
        return ''

    files = {'image_url[1]': (None, photo),
             'image_url[2]': (None, country_flag[country]),
             'image_url[3]': (None, city2stadium[city]),
             'template_name': (None, templates_names['stadium'])}

    response = requests.post(URL, files=files)

    return response.text


def post2photlab(photo, template):
    """
        Generate photo by template
        photos - url - str
        template - name of template - str
        example:
            url = 'http://www.wallpapersin4k.org/wp-content/uploads/2016/12/Man-Wallpapers-3.jpg'
            template_name = 'SOME_TEMPLATE
            print(post2photlab(url, template_name))
    """
    if not isinstance(photo, str):
        print('photos must be str')
        return ''

    if not isinstance(template, str):
        print('teams must be str')
        return ''

    if template not in templates_names:
        print('unknown name of template')

    files = {'image_url[1]': (None, photo),
             'template_name': (None, templates_names[template])}

    response = requests.post(URL, files=files)

    return response.text


def generate_city_photo(city):
    """
        Return url photo of city from yandex and url after photolab.
        city - str
    """
    city = 'красивые места ' + city
    search_city = "https://yandex.ru/images/search?text=" + city

    s = requests.get(search_city)
    b = bs4.BeautifulSoup(s.text, "html.parser")
    count = 0
    good_url = []
    for match in b.select('.serp-item__link'):
        url = match.get('href').split('=')[2]
        url = url.replace('%3A', ':').replace('%2F', '/').split('&')[0]
        if url[-4:] == '.jpg':
            count += 1
            good_url.append(url)
        if count == 10:
            break

    url = np.random.choice(good_url, 1)[0]
    template = 'nature_' + str(np.random.choice(range(1, 7)))

    new_url = post2photlab(url, template)

    return url, new_url
