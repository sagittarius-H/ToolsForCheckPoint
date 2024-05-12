import sqlite3

class Model:
    @staticmethod
    # метод для получения данных из dat файла базы данных
    def get_db_data(path: str, request: str):
        with sqlite3.connect(path) as connection:
            sql_exec = connection.cursor()
            sql_exec.execute(request)
            result = sql_exec.fetchall()
        return result
