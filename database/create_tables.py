import psycopg2
from psycopg2 import sql

from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def create_tables():
    """Создаёт таблицы companies и vacancies в базе данных PostgreSQL."""

    commands = (
        """
        CREATE TABLE IF NOT EXISTS companies (
            id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS vacancies (
            id SERIAL PRIMARY KEY,
            title VARCHAR NOT NULL,
            salary INTEGER,
            url TEXT,
            company_id INTEGER REFERENCES companies(id)
        )
        """
    )

    with psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
        host=DB_HOST, port=DB_PORT
    ) as conn:
        with conn.cursor() as cur:
            for command in commands:
                cur.execute(command)
        conn.commit()


if __name__ == "__main__":
    create_tables()
    print("Таблицы успешно созданы.")
