from typing import Optional


class Vacancy:
    """Класс для представления вакансии."""

    def __init__(self, vacancy_id: int, title: str, salary: Optional[int], url: str, company_id: int) -> None:
        self.vacancy_id = vacancy_id
        self.title = title
        self.salary = salary
        self.url = url
        self.company_id = company_id

    def __str__(self) -> str:
        salary = f"{self.salary}₽" if self.salary is not None else "не указана"
        return f"{self.title} — зарплата: {salary}"

    @classmethod
    def from_dict(cls, data: dict) -> "Vacancy":
        vacancy_id = int(data["id"])
        title = data["name"]
        salary = data.get("salary", {})
        salary_amount = salary.get("from") if salary else None
        url = data["alternate_url"]
        company_id = int(data["employer"]["id"])

        return cls(
            vacancy_id=vacancy_id,
            title=title,
            salary=salary_amount,
            url=url,
            company_id=company_id,
        )

    def save_to_db(self, conn) -> None:
        """Сохраняет объект вакансии в таблицу vacancies."""
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO vacancies (id, title, salary, url, company_id)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """,
                (self.vacancy_id, self.title, self.salary, self.url, self.company_id)
            )
        conn.commit()
