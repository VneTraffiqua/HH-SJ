import requests
from itertools import count
from dotenv import load_dotenv
import os
import copy
from terminaltables import AsciiTable


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        predicted_salary = (salary_from + salary_to) / 2
    elif salary_from:
        predicted_salary = salary_from * 1.2
    else:
        predicted_salary = salary_to * 0.8
    return predicted_salary


def get_language_statistics_hh(prog_language):
    salaries = []
    moscow_city_id = 1
    for page in count(0):
        url = 'https://api.hh.ru/vacancies'
        settings = {
            'page': page,
            'area': moscow_city_id,
            'text': prog_language,
        }
        response = requests.get(url, params=settings)
        response.raise_for_status()
        hh_vacancies = response.json()
        vacancies = hh_vacancies['items']
        for vacancy in vacancies:
            try:
                if vacancy['salary']['currency'] == 'RUR':
                    salaries.append(
                        predict_salary(
                            vacancy['salary']['from'],
                            vacancy['salary']['to']
                        )
                    )
                else:
                    salaries.append(None)

            except TypeError:
                salaries.append(None)

        if page >= hh_vacancies['pages'] - 1:
            break
    filtered_salaries = [solary for solary in salaries if solary]
    try:
        average_salary = int(sum(filtered_salaries) / len(filtered_salaries))
    except ZeroDivisionError:
        average_salary = 0
    return [
        prog_language,
        len(salaries),
        len(filtered_salaries),
        average_salary
    ]


def get_language_statistics_sj(
        programming_language,
        secret_key
):
    salaries = []
    number_of_vacancies_per_page = 100
    moscow_city_id = 4
    block_position_id = 1
    programmer_category_id = '48'
    for page in count(0):
        url = 'https://api.superjob.ru/2.0/vacancies/'
        headers = {
            'X-Api-App-Id': secret_key
        }

        params = {
            'count': number_of_vacancies_per_page,
            'page': page,
            't': moscow_city_id,
            'keywords': [
                [block_position_id, 'and', programming_language]
            ],
            'catalogues': [programmer_category_id, ],
            }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        sj_vacancies = response.json()
        vacancies = sj_vacancies.get('objects')
        number_of_page = sj_vacancies['total'] // number_of_vacancies_per_page
        for vacancy in vacancies:
            payment_from = vacancy['payment_from']
            payment_to = vacancy['payment_to']
            try:
                salaries.append(
                    predict_salary(payment_from, payment_to)
                )
            except TypeError:
                salaries.append(None)
        if page > number_of_page:
            break
    filtered_salaries = [salary for salary in salaries if salary]
    try:
        average_salary = int(sum(filtered_salaries) / len(filtered_salaries))
    except ZeroDivisionError:
        average_salary = 0
    return [
        programming_language,
        len(salaries),
        len(filtered_salaries),
        int(average_salary)
    ]


if __name__ == '__main__':
    load_dotenv()
    sj_secret_key = os.getenv('SJ_API')
    languages = (
        'JavaScript',
        'Java',
        'Python',
        'Ruby',
        'PHP',
        'C++',
        'C#',
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
    for language in languages:
        table_columns_HH.append(
            get_language_statistics_hh(language)
        )
        table_columns_SJ.append(
            get_language_statistics_sj(
                language, sj_secret_key
            )
        )
    print(AsciiTable(table_columns_HH, 'HeadHunter Moscow').table)
    print(AsciiTable(table_columns_SJ, 'SuperJob Moscow').table)
