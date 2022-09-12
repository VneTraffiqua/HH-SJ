import requests
from terminaltables import AsciiTable


def get_the_number_of_vacancies(area_id, keyword):
    url = 'https://api.hh.ru/vacancies'
    settings = {
        'area': area_id,
        'text': keyword
    }
    response = requests.get(url, params=settings)
    response.raise_for_status()
    return response.json()['found']


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
    return filtered_salaries


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
    found_list = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'],]
    for language in languages:
        salaries = predict_rub_salary(language)
        language_info = []
        language_info.append(language)
        language_info.append(get_the_number_of_vacancies(area_id, language))
        language_info.append(len(salaries))
        language_info.append(int(sum(salaries) / len(salaries)))
        found_list.append(language_info)

    title = 'HeadHunter Moscow'
    TABLE_DATA = found_list

    table_inst = AsciiTable(TABLE_DATA, title)
    print(table_inst.table)



