import requests
from terminaltables import AsciiTable


def predict_rub_salary(vacancy, area_id=1):
    url = 'https://api.hh.ru/vacancies'
    settings = {
        'area': area_id,
        'text': vacancy
    }
    response = requests.get(url, params=settings)
    response.raise_for_status()
    vacancies = response.json()['items']
    salaries = []
    for vacancy in vacancies:
        try:
            salaries.append(vacancy['salary']['from'])
        except TypeError:
            salaries.append(None)
    filtered_salaries = [solary for solary in salaries if solary is not None]
    return filtered_salaries, response.json()['found']


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
    area_id = 1
    found_list = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата'
        ],
    ]
    for language in languages:
        salaries, not_processed_vacancies = predict_rub_salary(language)
        language_info = []
        found_list.append(
            [
                language, not_processed_vacancies,
                len(salaries),
                int(sum(salaries) / len(salaries))
            ]
        )

    title = 'HeadHunter Moscow'

    table_inst = AsciiTable(found_list, title)
    print(table_inst.table)



