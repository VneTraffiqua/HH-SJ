import copy
import requests
import os
from dotenv import load_dotenv
from itertools import count
from terminaltables import AsciiTable


def get_found_vacancies_solary_count(text, area_id=1):
    salaries = []
    for page in count(0):
        url = 'https://api.hh.ru/vacancies'
        settings = {
            'page': page,
            'area': area_id,
            'text': text,
        }
        response = requests.get(url, params=settings)
        response.raise_for_status()
        hh_json = response.json()
        vacancies = hh_json['items']
        for vacancy in vacancies:
            try:
                salaries.append(vacancy['salary']['from'])
            except TypeError:
                salaries.append(None)
        if page >= hh_json['pages'] - 1:
            break
    filtered_salaries = [solary for solary in salaries if solary]
    return filtered_salaries, hh_json['found']


def all_sj_vacancies_by_id():
    load_dotenv()
    for page in count(0):
        url = 'https://api.superjob.ru/2.0/vacancies/'
        headers = {
            'X-Api-App-Id': os.getenv('SJ_API')
        }

        params = {
            'count': 100,
            'page': page,
            't': '4',
            'catalogues': ['48']
            }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        vacancies = response.json().get('objects')
        number_of_vacancies = response.json().get('total')
        number_of_page = number_of_vacancies // 100
        all_vacancies_by_id = []
        for vacancy in vacancies:
            all_vacancies_by_id.append(vacancy)
            if vacancy.get('payment_from') == 0:
                vacancy['payment_from'] = None
            yield vacancy
        if page >= number_of_page:
            break


if __name__ == '__main__':
    languages = (
        'JavaScript',
        'Java',
        'Python',
        'Ruby',
        'PHP',
        'C++',
        'C#',
        'TypeScript',
        'Go',
        '1С'
    )
    table_columns_HH = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата'
        ],
    ]
    table_columns_SJ = copy.deepcopy(table_columns_HH)
    sorted_vacancies_sj_for_language = {}
    for language in languages:
        salaries, not_processed_vacancies = get_found_vacancies_solary_count(
            language
        )
        if salaries:
            table_columns_HH.append(
                [
                    language, not_processed_vacancies,
                    len(salaries),
                    int(sum(salaries) / len(salaries))
                ]
            )

        sorted_vacancies_sj_for_language[language] = []
        for vacancy in all_sj_vacancies_by_id():
            if language in vacancy['profession']:
                sorted_vacancies_sj_for_language[language].append(vacancy)

    for key, value in sorted_vacancies_sj_for_language.items():
        vacancies_processed = 0
        all_solary = 0
        for vacancy in value:
            if vacancy.get('payment_from'):
                vacancies_processed += 1
                all_solary += vacancy.get('payment_from')
        table_columns_SJ.append(
            [
                key, len(value),
                vacancies_processed,
                (
                    int(all_solary / vacancies_processed)
                    if vacancies_processed > 0
                    else 0
                    )
            ]
        )

    print(AsciiTable(table_columns_HH, 'HeadHunter Moscow').table)
    print(AsciiTable(table_columns_SJ, 'SuperJob Moscow').table)
