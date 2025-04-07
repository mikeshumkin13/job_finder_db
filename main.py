from database.create_database import create_database
from database.create_tables import create_tables

if __name__ == "__main__":
    create_database()
    create_tables()

from api.hh_api import get_vacancies_by_employer_id  # Импортируем функцию из API


if __name__ == "__main__":
    # Пример ID компании на HH (Яндекс = 1740)
    employer_id = 1740

    # Получаем вакансии
    vacancies = get_vacancies_by_employer_id(employer_id, per_page=5)

    # Выводим названия вакансий
    for i, vacancy in enumerate(vacancies.get("items", []), 1):
        print(f"{i}. {vacancy['name']}")
