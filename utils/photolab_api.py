import requests
import bs4
import numpy as np
import os
from utils.used_dict import *
from random import randint

post_types = ['stadium',
              'faceball',
              'versus',
              'goal',
              'miss',
              'city_info',
              'final_post'
              ]

def post_photolab_photo(post_type, args):
    """
           Generate photo
           post_type - type from post_types list
           args - list of urls photos as type str

           example:
                post_type = 'stadium'
                args = ['Moscow', 'http://www.wallpapersin4k.org/wp-content/uploads/2016/12/Man-Wallpapers-3.jpg',
                'http://games-of-thrones.ru/sites/default/files/pictures/all/Ben%20Affleck/28.jpg']
    """
    if not isinstance(post_type, str):
        print('post type must be str')
        return ''

    if not isinstance(post_type, list):
        print('post type must be list')
        return ''

    if post_type not in post_types:
        print('unknown type')
        return ''

    return eval("post2photlab" + post_type)(*args)

def post2photlab_versus(photos: object, teams: object) -> object:
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


def post2photlab_final_post(photos, team, stadium):
    """
    Generate final photo with users
    photos - list of urls of users as type str
    team - name of country in English
    
    example:
    11 urls of users
    photos = ['http://kinodom.org/uploads/posts/2013-03/1364165379_1691665...; for i in range(11)]
    print(post2photlab_final_post(photos, 'Russia', 'Москва'))
    """
    if not isinstance(photos, list):
        print('photos must be list')
        return ''

    if len(photos) != 11:
        print('len photos must be equal 11')
        return ''

    if team not in country_flag:
        print('unknown country ' + team)
        return ''

    urls = []
    for i in range(11):
        urls.append(photos[i])
    urls.append(country_flag[team])
    urls.append(city2stadium[stadium])

    files = {}
    for i in range(13):
        files['image_url['+str(i+1)+']'] = (None, urls[i])

    files['template_name'] = (None, templates_names['final_post'])

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

def get_picture(search_request):
    headers = {
        'Ocp-Apim-Subscription-Key': '19b79738abc145beac38e42819f80c23',
    }

    params = {
        'q': search_request,
        'count': '10',
        'offset': '0',
        'mkt': 'en-us',
        'safeSearch': 'Moderate',
    }

    response = requests.get(
        'https://api.cognitive.microsoft.com/bing/v7.0/images/search?%s',
        params=params,
        headers=headers
    )

    if response.status_code != 200:
        response.raise_for_status()

    try:
        picture_url = response.json()['value'][randint(0, 7)]['contentUrl']
    except IndexError or KeyError:
        try:
            picture_url = response.json()['value'][0]['contentUrl']
        except IndexError or KeyError:
            picture_url = None

    return picture_url

def post2photolab_city_info(city):
    """
        Return url photo of city from yandex and url after photolab.
        city - str
    """

    url = get_picture(city)
    template = 'nature_' + str(np.random.choice(range(1, 7)))

    new_url = post2photlab(url, template)

    return url, new_url











