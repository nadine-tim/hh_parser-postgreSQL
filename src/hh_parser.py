import requests


class HeadHunterAPI:
    """
    Класс для подключения к API HeadHunter и получения вакансий от 10 работодателей
    """

    def __init__(self):
        self.name = "HeadHunter"
        self.url = 'https://api.hh.ru/vacancies?employer_id='
        self.employers_id = ["625332", "9544277", "1236698", "172", "4013696", "546422", "157761", "72995", "9098461",
                             "113121"]

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}')"

    def get_vacancies(self, employer_id):
        """
        Парсинг вакансий с HH
        """
        vacancy_list = []
        pages_number = 0
        page = 1
        while pages_number < page:
            params = {
                # 'text': text,  # Текст фильтра. В имени должно быть слово "Аналитик"
                'page': pages_number,  # Индекс страницы поиска на HH
                'per_page': 100  # Кол-во вакансий на 1 странице
            }

            hh_request = {}
            try:
                hh_request = requests.get(self.url + employer_id, params=params)  # Посылаем запрос к API
            except requests.HTTPError:
                print("bad response from hh.ru")

            if hh_request is None or hh_request.status_code != 200:
                return []
            else:
                hh_vacancies = hh_request.json()['items']

            for vacancy in hh_vacancies:
                salary_from, salary_to, currency = self.get_salary(vacancy['salary'])
                vacancy_list.append({
                    'id': vacancy['id'],
                    'vacancy': vacancy['name'],
                    'employer_id': vacancy['employer']['id'],
                    'employer': vacancy['employer']['name'],
                    'salary_from': salary_from,
                    'salary_to': salary_to,
                    'currency': currency,
                    'url': vacancy['alternate_url']
                })
            pages_number += 1
        #     print(f'Поиск на hh.ru , номер страницы: {pages_number}')
        # print(f'найдено вакансий: {len(vacancy_list)}')
        return vacancy_list

    def get_employers_vacancies(self):
        all_vacancies = []

        for i in self.employers_id:
            try:
                vacancies = self.get_vacancies(i)
                all_vacancies.extend(vacancies)
            except:
                print("Ошибка заполнения данных о работодателе")
        return all_vacancies

    @staticmethod
    def get_salary(salary):
        """
        Проверка наличия указания з/п вилки
        """
        salary_gross = [None, None, None]
        if salary and salary['from'] and salary['from'] != 0:
            salary_gross[0] = salary['from']
        if salary and salary['to'] and salary['to'] != 0:
            salary_gross[1] = salary['to']
        if salary and salary['currency']:
            salary_gross[2] = salary['currency']
        return salary_gross
