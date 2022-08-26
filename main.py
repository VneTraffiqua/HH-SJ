import requests
#59455818 - user id


def main():
    url = 'https://api.hh.ru/vacancies' #'https://api.hh.ru/'
    settings = {
        'area': '1',
    }
    response = requests.get(url, params=settings)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    print(main())


