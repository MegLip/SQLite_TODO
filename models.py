import sqlite3
from sqlite3 import Error


class Todos:

    def __init__(self, database):
        self.conn = None

        try:
            self.conn = sqlite3.connect(database, check_same_thread=False)
            if self.conn is not None:
                self.conn.cursor().execute("""CREATE TABLE IF NOT EXISTS todos (
                                            id integer PRIMARY KEY,
                                            title VARCHAR(250) NOT NULL,
                                            description TEXT,
                                            done BIT);""")
            self.cur = self.conn.cursor()
        except Error as e:
            print(e)

    def all(self):
        result = self.cur.execute("SELECT * FROM todos")
        return result.fetchall()

    def get(self, id):
        result = self.cur.execute(f"SELECT * FROM todos WHERE id={id}")
        return result.fetchone()

    def create(self, data):
        sql = '''INSERT INTO todos(title, description, done)
                    VALUES(?,?,?)'''
        result = self.cur.execute(sql, data)
        self.conn.commit()
        return result.lastrowid

    def update(self, id, data):
        sql = f''' UPDATE todos
                    SET title = ?, description = ?, done = ?
                    WHERE id = {id}'''
        print(id)

        try:
            self.cur.execute(sql, data)
            self.conn.commit()
        except sqlite3.OperationalError as e:
            print(e)

    def delete_where(self, **kwargs):
        qs = []
        values = tuple()
        for k, v in kwargs.items():
            qs.append(f"{k}=?")
            values += (v,)
        q = " AND ".join(qs)

        sql = f'DELETE FROM todos WHERE {q}'
        cur = self.conn.cursor()
        cur.execute(sql, values)
        self.conn.commit()
        print("Deleted")


database = "database.db"
todos = Todos(database)

if __name__ == "__main__":
    todos = Todos("database.db")
