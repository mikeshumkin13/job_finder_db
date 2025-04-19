class Company:
    """Класс для представления компании."""

    def __init__(self, company_id: int, name: str) -> None:
        self.company_id = company_id
        self.name = name

    def __str__(self) -> str:
        return f"{self.name} (ID: {self.company_id})"

    @classmethod
    def from_dict(cls, data: dict) -> "Company":
        company_id = int(data["id"])
        name = data["name"]
        return cls(company_id, name)

    def save_to_db(self, conn) -> None:
        """Сохраняет объект компании в таблицу companies."""
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO companies (id, name)
                VALUES (%s, %s)
                ON CONFLICT (id) DO NOTHING
                """,
                (self.company_id, self.name)
            )
        conn.commit()
