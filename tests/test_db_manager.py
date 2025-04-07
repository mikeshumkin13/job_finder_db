import pytest
from storage.db_manager import DBManager


@pytest.fixture(scope="module")
def db_manager():
    """Фикстура для подключения к базе данных."""
    return DBManager()

def test_get_companies_and_vacancies_count(db_manager):
    result = db_manager.get_companies_and_vacancies_count()
    assert isinstance(result, list)
    assert all(isinstance(item, str) for item in result)
    assert any("вакансий" in item for item in result)

def test_get_all_vacancies(db_manager):
    result = db_manager.get_all_vacancies()
    assert isinstance(result, list)
    assert all(isinstance(item, str) for item in result)
    assert any("| зарплата:" in item for item in result)

def test_get_avg_salary(db_manager):
    avg_salary = db_manager.get_avg_salary()
    assert isinstance(avg_salary, int)
    assert avg_salary >= 0

def test_get_vacancies_with_higher_salary(db_manager):
    result = db_manager.get_vacancies_with_higher_salary()
    assert isinstance(result, list)
    assert all(isinstance(row, tuple) for row in result)
    if result:
        assert len(result[0]) == 4  # company, title, salary, url

def test_get_vacancies_with_keyword(db_manager):
    result = db_manager.get_vacancies_with_keyword("python")
    assert isinstance(result, list)
    assert all(isinstance(item, str) for item in result)

