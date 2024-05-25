import sqlite3


class Model:
    @staticmethod
    # Метод для получения данных из dat файла базы данных
    def get_db_data(path: str, request: str) -> list:
        with sqlite3.connect(path) as connection:
            sql_exec = connection.cursor()
            sql_exec.execute(request)
            result = sql_exec.fetchall()
        return result
