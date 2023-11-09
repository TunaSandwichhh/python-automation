import sqlite3
from sqlite3 import Error

class NotificationLogDB:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = self.create_connection()

        if self.conn:
            self.create_table()

    def create_connection(self):
        """Create a database connection to the SQLite database"""
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            print(e)
            raise e

    def create_table(self):
        """Create a table in the SQLite database to log notifications"""
        try:
            sql = """CREATE TABLE IF NOT EXISTS notifications_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        task_id INTEGER NOT NULL,
                        notification_type TEXT NOT NULL,
                        sent_datetime TEXT NOT NULL,
                        status TEXT NOT NULL,
                        FOREIGN KEY (task_id) REFERENCES tasks (id)
                     );"""
            self.conn.execute(sql)
        except Error as e:
            print(e)

    def log_notification(self, task_id, notification_type, sent_datetime, status):
        """Log a notification event to the notifications_log table"""
        sql = '''INSERT INTO notifications_log(task_id, notification_type, sent_datetime, status)
                 VALUES (?, ?, ?, ?)'''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (task_id, notification_type, sent_datetime, status))
            self.conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(e)

    def get_notification_logs(self, task_id=None):
        """Query notification logs by task_id"""
        sql = "SELECT * FROM notifications_log"
        params = ()
        if task_id:
            sql += " WHERE task_id = ?"
            params = (task_id,)
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(e)
    
    def close_connection(self):
        """Close the database connection"""
        try:
            self.conn.close()
        except Error as e:
            print(e)