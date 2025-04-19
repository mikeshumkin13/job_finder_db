import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def create_database():
    """Создаёт базу данных job_finder, если она не существует."""
    try:
        # подключение без указания базы
        conn = psycopg2.connect(
            dbname="postgres",  # подключаемся к системной БД
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        with conn.cursor() as cur:
            cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
            exists = cur.fetchone()
            if not exists:
                cur.execute(f"CREATE DATABASE {DB_NAME}")
                print(f"База данных {DB_NAME} успешно создана.")
            else:
                print(f"База данных {DB_NAME} уже существует.")

        conn.close()
    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")


if __name__ == "__main__":
    create_database()
