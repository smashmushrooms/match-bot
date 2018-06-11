import requests

TEMPLATE_VERSUS = 'VERSUS'
URL = 'http://api-hack.photolab.me/template_process.php'


def post2photlab_versus(photos, teams):
    url1 = photos[0]
    url2 = photos[1]
    url3 = teams[0]
    url4 = teams[1]

    files = {'image_url[1]': (None, url1),
             'image_url[2]': (None, url2),
             'image_url[3]': (None, url3),
             'image_url[4]': (None, url4),
             'template_name': (None, TEMPLATE_VERSUS)}

    response = requests.post(URL, files=files)

    return response


def post2photlab(photo, template):
    files = {'image_url[1]': (None, photo),
             'template_name': (None, template)}

    response = requests.post(URL, files=files)

    return response


def post2photlab_without(photos):
    url1 = photos[0]
    url2 = photos[1]

    files = {'image_url[1]': (None, url1),
             'image_url[2]': (None, url2),
             'template_name': (None, 'CEAEF9D1-B95D-0804-9D87-5C5FAEF2F0E7')}

    response = requests.post(URL, files=files)

    return response


if __name__ == "__main__":
    print("Start")
    url1 = 'https://static.life.ru/posts/2015/05/154452/gr/north/46a347254c68de2ae3badabcca0c6ae5__1200x630.jpg'
    url2 = 'https://bzns.media/upload/resize_cache/iblock/646/932_932_1/646eac2be210ed63fcf645f32f3712e5.jpg'
    print(post2photlab_without([url1, url2]).text)
