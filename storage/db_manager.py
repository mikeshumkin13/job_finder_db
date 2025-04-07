import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


class DBManager:
    """Класс для взаимодействия с базой данных PostgreSQL."""

    def __init__(self) -> None:
        """Инициализирует подключение к базе данных."""
        self.conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

    def get_companies_and_vacancies_count(self) -> list[str]:
        """
        Получает список всех компаний и количество вакансий у каждой из них.

        :return: Список строк с названием компании и количеством вакансий
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT c.name, COUNT(v.id) AS vacancies_count
                FROM companies c
                LEFT JOIN vacancies v ON c.id = v.company_id
                GROUP BY c.name
                ORDER BY vacancies_count DESC;
                """
            )
            results = cur.fetchall()

        return [f"{name}: {count} вакансий" for name, count in results]



    def get_all_vacancies(self) -> list[str]:
        """
        Получает список всех вакансий с названием компании, вакансии, зарплатой и ссылкой.

        :return: Список строк с описанием каждой вакансии.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT c.name, v.title, v.salary, v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.id
                ORDER BY v.salary DESC NULLS LAST;
                """
            )
            rows = cur.fetchall()

        result = []
        for company, title, salary, url in rows:
            salary_str = f"{salary}₽" if salary is not None else "не указана"
            result.append(f"{company} | {title} | зарплата: {salary_str} | ссылка: {url}")
        return result


    def get_avg_salary(self) -> int:
        """
        Получает среднюю зарплату по всем вакансиям (где она указана).

        :return: Средняя зарплата (округлённая).
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT AVG(salary) FROM vacancies WHERE salary IS NOT NULL;
                """
            )
            result = cur.fetchone()
        return int(result[0]) if result[0] is not None else 0



    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.

        :return: Список кортежей (компания, вакансия, зарплата, ссылка).
        """
        with self.conn.cursor() as cur:
            # Получаем среднюю зарплату
            avg_salary = self.get_avg_salary()

            # Выполняем SQL-запрос
            cur.execute(
                """
                SELECT companies.name, vacancies.title, vacancies.salary, vacancies.url
                FROM vacancies
                JOIN companies ON vacancies.company_id = companies.id
                WHERE vacancies.salary > %s;
                """,
                (avg_salary,)
            )

            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> list[str]:
        """
        Получает список всех вакансий, в названии которых содержится переданное слово.

        :param keyword: Ключевое слово для поиска в названии вакансии.
        :return: Список строк с описанием найденных вакансий.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT companies.name, vacancies.title, vacancies.salary, vacancies.url
                FROM vacancies
                JOIN companies ON vacancies.company_id = companies.id
                WHERE LOWER(vacancies.title) LIKE %s;
                """,
                (f"%{keyword.lower()}%",)
            )
            results = cur.fetchall()

        return [
            f"{company} | {title} | зарплата: {salary if salary else 'не указана'} | ссылка: {url}"
            for company, title, salary, url in results
        ]

