import requests


def get_vacancies_by_employer_id(employer_id: int, page: int = 0, per_page: int = 20) -> dict:
    """
    Получает вакансии по ID работодателя с сайта hh.ru.

    :param employer_id: ID компании на hh.ru
    :param page: номер страницы (по умолчанию 0)
    :param per_page: количество вакансий на странице (по умолчанию 20)
    :return: словарь с результатами вакансий
    """
    url = "https://api.hh.ru/vacancies"
    params = {
        "employer_id": employer_id,
        "page": page,
        "per_page": per_page
    }

    response = requests.get(url, params=params)
    response.raise_for_status()  # выбросит ошибку, если код ответа не 200
    return response.json()
