from database.create_database import create_database
from database.create_tables import create_tables
from api.hh_api import get_vacancies_by_employer_id
from models.company import Company
from models.vacancy import Vacancy
from storage.db_manager import DBManager
import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def save_data_to_database(employer_ids: list[int]) -> None:
    """
    Получает данные с API и сохраняет в базу данных.
    """
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )

        for employer_id in employer_ids:
            vacancies_data = get_vacancies_by_employer_id(employer_id, per_page=20)
            if not vacancies_data.get("items"):
                continue

            company = Company.from_dict(vacancies_data["items"][0]["employer"])
            company.save_to_db(conn)

            vacancies = [
                Vacancy.from_dict(item)
                for item in vacancies_data.get("items", [])
            ]
            for vacancy in vacancies:
                vacancy.save_to_db(conn)

        conn.close()
        print("✅ Данные успешно сохранены в базу данных.")

    except Exception as e:
        print(f"❌ Ошибка при сохранении данных: {e}")


def user_interface():
    """
    Простой CLI-интерфейс для пользователя.
    """
    db = DBManager()

    while True:
        print("\n=== Меню ===")
        print("1 - Показать компании и количество вакансий")
        print("2 - Показать все вакансии")
        print("3 - Показать среднюю зарплату")
        print("4 - Показать вакансии с зарплатой выше средней")
        print("5 - Найти вакансии по ключевому слову")
        print("0 - Выход")

        choice = input("Введите номер действия: ")

        if choice == "1":
            for line in db.get_companies_and_vacancies_count():
                print(line)

        elif choice == "2":
            for line in db.get_all_vacancies():
                print(line)

        elif choice == "3":
            print(f"Средняя зарплата по всем вакансиям: {db.get_avg_salary()} ₽")

        elif choice == "4":
            for line in db.get_vacancies_with_higher_salary():
                print(line)

        elif choice == "5":
            keyword = input("Введите ключевое слово для поиска: ")
            for line in db.get_vacancies_with_keyword(keyword):
                print(line)

        elif choice == "0":
            print("👋 До свидания!")
            break

        else:
            print("❗ Неверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    # 1. Создаём БД и таблицы
    create_database()
    create_tables()

    # 2. Указываем 10 employer_id (компаний)
    employer_ids = [
        1740,    # Яндекс
        3529,    # Сбер
        78638,   # VK
        15478,   # Ozon
        64174,   # Тинькофф
        4181,    # МТС
        907345,  # Альфа-банк
        1002342, # Лаборатория Касперского
        3127,    # Mail.ru
        1002782  # Avito
    ]

    # 3. Получаем и сохраняем данные
    save_data_to_database(employer_ids)

    # 4. Запускаем интерфейс пользователя
    user_interface()
