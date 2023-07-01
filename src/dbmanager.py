"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2


class DBManager:
    """
    Класс для подключения к БД Postgres и получения статистики по вакансиям и работодателям
    """

    def __init__(self):
        self.host = 'localhost'
        self.database = "hh_vacancies"
        self.user = 'postgres'
        self.password = 'pgadmin'
        self.port = '5432'

    def create_db(self):
        """
        Создает БД
        """
        params = {
            'host': self.host,
            'user': self.user,
            'password': self.password,
            'dbname': 'postgres'
        }
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        conn.autocommit = True
        cur.execute(f"DROP DATABASE IF EXISTS {self.database} WITH (FORCE)")
        cur.execute(f"CREATE DATABASE {self.database}")
        cur.close()
        conn.close()

        table_params = {
            'host': self.host,
            'user': self.user,
            'password': self.password,
            'dbname': self.database
        }
        conn = psycopg2.connect(**table_params)
        cur = conn.cursor()

        cur.execute("""
                    CREATE TABLE vacancies (
                        id INT PRIMARY KEY,
                        vacancy VARCHAR(100),
                        employer_id INT,
                        employer VARCHAR(100),
                        salary_from INT,
                        salary_to INT,
                        currency VARCHAR(10),
                        url VARCHAR(255)
                    )
                """)
        cur.close()
        conn.commit()
        conn.close()

    def insert_vacancies_db(self, vacancies_list):

        params = {
            'host': self.host,
            'user': self.user,
            'password': self.password,
            'dbname': self.database
        }
        conn = psycopg2.connect(**params)

        for vacancy in vacancies_list:
            cur = conn.cursor()
            placeholders = ', '.join(['%s'] * len(vacancy))
            columns = ', '.join(vacancy.keys())
            sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ('vacancies', columns, placeholders)
            cur.execute(sql, list(vacancy.values()))
            cur.close()

        conn.commit()
        conn.close()

    @staticmethod
    def get_companies_and_vacancies_count():
        """
        Получает список всех компаний и количество вакансий у каждой компании
        """
        query = 'SELECT employer, COUNT(vacancy) FROM vacancies GROUP BY employer'
        conn = psycopg2.connect(host='localhost', database='hh_vacancies', user='postgres', password='pgadmin')
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                data = cur.fetchall()
        data_dict = [{"name": d[0], "count": d[1]} for d in data]
        return data_dict

    @staticmethod
    def get_all_vacancies():
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        """
        query = 'SELECT vacancy, employer, salary_from, salary_to, currency, url FROM vacancies'
        conn = psycopg2.connect(host='localhost', database='hh_vacancies', user='postgres', password='pgadmin')
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                data = cur.fetchall()
        data_dict = [{"name": d[0], "vacancy": d[1], "salary_to": d[2], "salary_from": d[3], "url": d[4]} for d in data]
        return data_dict

    @staticmethod
    def get_avg_salary():
        """
        Получает среднюю зарплату по вакансиям
        """
        query = 'SELECT ROUND(AVG(salary_to) + AVG(salary_from))/2 FROM vacancies WHERE salary_to !=0 OR salary_from ' \
                '!=0'
        conn = psycopg2.connect(host='localhost', database='hh_vacancies', user='postgres', password='pgadmin')
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                data = cur.fetchall()
        data_dict = [{"salary_avg": d[0]} for d in data]
        return data_dict

    @staticmethod
    def get_vacancies_with_higher_salary():
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        query = 'SELECT vacancy, salary_from, salary_to FROM vacancies GROUP BY vacancy, salary_from, salary_to ' \
                'HAVING (SELECT ROUND(AVG(salary_to) + AVG(salary_from))/2 FROM vacancies WHERE salary_to !=0 OR ' \
                'salary_from !=0) < salary_to OR (SELECT ROUND(AVG(salary_to) + AVG(salary_from))/2 FROM vacancies  ' \
                'WHERE salary_to !=0 OR salary_from !=0) < salary_from'
        conn = psycopg2.connect(host='localhost', database='hh_vacancies', user='postgres', password='pgadmin')
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                data = cur.fetchall()
        data_dict = [{"vacancies": d[0]} for d in data]
        return data_dict

    @staticmethod
    def get_vacancies_with_keyword(word):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”
        """
        keyword = "'" + '%' + word + '%' + "'"
        query = f'SELECT vacancy FROM vacancies WHERE vacancy LIKE {keyword}'
        conn = psycopg2.connect(host='localhost', database='hh_vacancies', user='postgres', password='pgadmin')
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                data = cur.fetchall()
        data_dict = [{"vacancies": d[0]} for d in data]
        return data_dict
