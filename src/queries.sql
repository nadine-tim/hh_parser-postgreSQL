-- """ получает список всех компаний и количество вакансий у каждой компании"""
SELECT employer, COUNT(vacancy)
FROM vacancies
GROUP BY employer

--"""получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
SELECT vacancy, employer, salary_from, salary_to, currency, url
FROM vacancies

--получает среднюю зарплату по вакансиям.
SELECT ROUND(AVG(salary_to) + AVG(salary_from))/2
FROM vacancies
WHERE salary_to !=0 OR salary_from !=0

--получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
SELECT vacancy, salary_from, salary_to
FROM vacancies
GROUP BY vacancy, salary_from, salary_to
HAVING (SELECT (AVG(salary_to) + AVG(salary_from))/2  FROM vacancies  WHERE salary_to !=0 OR salary_from !=0)  < salary_to
OR (SELECT (AVG(salary_to) + AVG(salary_from))/2  FROM vacancies  WHERE salary_to !=0 OR salary_from !=0) < salary_from


--"""получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”"""
SELECT vacancy
FROM vacancies
WHERE vacancy ILIKE {keyword}