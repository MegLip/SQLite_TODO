import sqlite3
from sqlite3 import Error


class Todos:
    # Łączymy się z bazą
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

    def get(self, todo_id):
        result = self.cur.execute(f"SELECT * FROM todos WHERE id={todo_id}")
        return result.fetchone()

    def create(self, data):
        sql = '''INSERT INTO todos(title, description, done)
                    VALUES(?,?,?)'''
        result = self.cur.execute(sql, data)
        self.conn.commit()
        return result.lastrowid

    def update(self, data, todo_id):
        sql = f''' UPDATE todos
                    SET title = ?, description = ?, done = ?
                    WHERE id={todo_id}'''
        print(todo_id)
        try:
            self.cur.execute(sql, data)
            self.conn.commit()
        except sqlite3.OperationalError as e:
            print(e)

    def delete(self, todo_id):
        """
        Delete a task by task id
        :param conn:  Connection to the SQLite database
        :param id: id of the task
        :return:
        """
        to_delete = self.cur.execute(f"DELETE FROM todos WHERE id={todo_id}")
        self.conn.commit()
        return to_delete

database = "database.db"
todos = Todos(database)
