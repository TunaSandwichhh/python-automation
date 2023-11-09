import sqlite3
from sqlite3 import Error

class TaskDatabase:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = self.create_connection()

        if self.conn:
            self.create_table()

    def create_connection(self):
        """Create a database connection to a SQLite database"""
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            print(e)
        return None

    def create_table(self):
        """Create a table in the SQLite database"""
        try:
            sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        description TEXT NOT NULL,
                                        due_date TEXT NOT NULL,
                                        status INTEGER NOT NULL DEFAULT 0
                                    );"""
            cursor = self.conn.cursor()
            cursor.execute(sql_create_tasks_table)
        except Error as e:
            print(e)

    def add_task(self, description, due_date, status=0):
        """Add a new task to the tasks table"""
        sql = ''' INSERT INTO tasks(description, due_date, status)
                  VALUES(?,?,?) '''
        cursor = self.conn.cursor()
        cursor.execute(sql, (description, due_date, status))
        self.conn.commit()
        return cursor.lastrowid

    def update_task(self, task_id, description, due_date, status):
        """Update status of a task in the tasks table"""
        sql = ''' UPDATE tasks
                  SET description = ?,
                      due_date = ?,
                      status = ?
                  WHERE id = ?'''
        cursor = self.conn.cursor()
        cursor.execute(sql, (description, due_date, status, task_id))
        self.conn.commit()

    def delete_task(self, task_id):
        """Delete a task from the tasks table by task id"""
        sql = 'DELETE FROM tasks WHERE id=?'
        cursor = self.conn.cursor()
        cursor.execute(sql, (task_id,))
        self.conn.commit()

    def get_task(self, task_id):
        """Query tasks by id"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,))

        row = cursor.fetchone()
        return row

    def get_all_tasks(self):
        """Query all rows in the tasks table"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tasks")

        rows = cursor.fetchall()
        return rows

    def close_connection(self):
        """Close the database connection"""
        try:
            self.conn.close()
        except Error as e:
            print(e)