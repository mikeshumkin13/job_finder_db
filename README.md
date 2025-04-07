#  Проект: Поиск вакансий с подключением к БД PostgreSQL

## 📄 Описание

Проект разработан в рамках обучения на курсе **"Профессия Python-разработчик"** в Skypro.  
Программа получает данные о вакансиях и компаниях с сайта [hh.ru](https://hh.ru) через API и сохраняет их в базу данных PostgreSQL.  
Затем пользователь может получать различную статистику по вакансиям, компаниям и зарплатам через текстовое меню.

---

## 🧱 Технологии

- Python 3.12
- PostgreSQL
- psycopg2
- requests
- pytest
- Poetry (для управления зависимостями)

---

## 🗃️ Структура проекта

job_finder_db % tree
.
├── README.md
├── __pycache__
│   └── config.cpython-312.pyc
├── api
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-312.pyc
│   │   └── hh_api.cpython-312.pyc
│   └── hh_api.py
├── config.py
├── database
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-312.pyc
│   │   ├── create_database.cpython-312.pyc
│   │   └── create_tables.cpython-312.pyc
│   ├── create_database.py
│   └── create_tables.py
├── job_finder_db
│   └── __init__.py
├── main.py
├── models
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-312.pyc
│   │   ├── company.cpython-312.pyc
│   │   └── vacancy.cpython-312.pyc
│   ├── company.py
│   └── vacancy.py
├── poetry.lock
├── pyproject.toml
├── storage
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-312.pyc
│   │   └── db_manager.cpython-312.pyc
│   └── db_manager.py
└── tests
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-312.pyc
    │   └── test_db_manager.cpython-312-pytest-8.3.5.pyc
    └── test_db_manager.py

13 directories, 31 files


---

## 🧠 Возможности

✅ Автоматическое создание базы данных и таблиц  
✅ Загрузка данных о вакансиях по 10 работодателям  
✅ Сохранение вакансий и компаний в PostgreSQL  
✅ Получение статистики и информации через текстовый интерфейс:

1. Список компаний и количество вакансий у каждой
2. Список всех вакансий (название компании, зарплата, ссылка)
3. Средняя зарплата по всем вакансиям
4. Вакансии с зарплатой выше средней
5. Поиск вакансий по ключевому слову

---

## 🚀 Как запустить

### 1. Клонируйте репозиторий:

git clone git@github.com:mikeshumkin13/job_finder_db.git
cd job_finder_db


## 2. Установите зависимости:
poetry install

## 3. Убедитесь, что PostgreSQL запущен и параметры в config.py указаны верно.

## 4. Запустите проект:
poetry run python main.py

# Тестирование
poetry run pytest tests/

# Автор
### mikeshumkin13
Проект выполнен в рамках обучения в Skypro.
