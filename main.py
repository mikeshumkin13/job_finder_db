import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from database.create_database import create_database
from database.create_tables import create_tables
from api.hh_api import get_vacancies_by_employer_id
from models.vacancy import Vacancy
from models.company import Company


if __name__ == "__main__":
    # Шаг 1: Создаём базу данных и таблицы, если их ещё нет
    create_database()
    create_tables()

    # Шаг 2: Получаем данные с API HH.ru
    employer_id = 1740  # Пример: Яндекс
    vacancies_data = get_vacancies_by_employer_id(employer_id, per_page=5)

    # Шаг 3: Создаём объект компании из первого элемента
    company = Company.from_dict(vacancies_data["items"][0]["employer"])

    # Шаг 4: Создаём список объектов вакансий
    vacancies = [
        Vacancy.from_dict(item)
        for item in vacancies_data.get("items", [])
    ]

    # Шаг 5: Выводим информацию
    print(company)
    print()
    for vacancy in vacancies:
        print(vacancy)

    # Шаг 6: Сохраняем данные в базу
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )

        company.save_to_db(conn)

        for vacancy in vacancies:
            vacancy.save_to_db(conn)

        conn.close()
        print("Данные успешно сохранены в базу данных.")

    except Exception as e:
        print(f"Ошибка при сохранении данных в базу: {e}")

