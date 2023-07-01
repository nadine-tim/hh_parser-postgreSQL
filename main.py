from src.hh_parser import HeadHunterAPI
from src.dbmanager import DBManager


def main():

    db_manager = DBManager()
    db_manager.create_db()
    api = HeadHunterAPI()
    vacancy_list = api.get_employers_vacancies()
    db_manager.insert_vacancies_db(vacancy_list)

    print("Данные по вакансиям были сохранены в БД")

    line2 = "Для вывода статистики по вакансиям, выберите действие: "
    line3 = "1-получить список всех компаний и количество вакансий у каждой компании"
    line4 = "2-получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"
    line5 = "3-получить среднюю зарплату по вакансиям"
    line6 = "4-получить список всех вакансий, у которых зарплата выше средней по всем вакансиям"
    line7 = "5-получить список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”"
    line8 = "exit-для завершения работы"

    user_print = [line2, line3, line4, line5, line6, line7, line8]
    print(*user_print, sep='\n')
    user_input = input("Введите значение: ").lower()

    while user_input != "exit":
        if user_input == '1':
            result = db_manager.get_companies_and_vacancies_count()
            for data in result:
                print(f"В компании {data['name']}: {data['count']} вакансий")
        elif user_input == '2':
            result = db_manager.get_all_vacancies()
            for data in result:
                print(f"В компании: {data['name']}, вакансия: {data['vacancy']}, зарплата: {data['salary_to']} рублей, ссылка на вакансию: {data['url']} ")
        elif user_input == '3':
            result = db_manager.get_avg_salary()
            for data in result:
                print(f"Средняя зарплата по вакансиям: {int(data['salary_avg'])}")
        elif user_input == '4':
            result = db_manager.get_vacancies_with_higher_salary()
            for data in result:
                print(f" {data['vacancies']}")
        elif user_input == '5':
            word = input("Введите ключевое слово для поиска: ")
            result = db_manager.get_vacancies_with_keyword(word)
            for data in result:
                print(f" {data['vacancies']}")
        else:
            print('Нет такого значения. Выберите из списка')

        print()
        print(*user_print, sep='\n')
        user_input = input("Введите значение: ").lower()


if __name__ == '__main__':
    main()
