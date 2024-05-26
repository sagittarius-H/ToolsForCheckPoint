import sqlite3


class Model:
    @staticmethod
    # Метод для получения данных из dat файла базы данных
    def get_db_data(path: str, request: str, data=None) -> list:
        with sqlite3.connect(path) as connection:
            sql_exec = connection.cursor()
            if data:
                sql_exec.execute(request, data)
            else:
                sql_exec.execute(request)
            result = sql_exec.fetchall()
        return result
