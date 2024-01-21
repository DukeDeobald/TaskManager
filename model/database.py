import sqlite3

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            self.initialize_database()
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise

    def initialize_database(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                due_date TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS completed_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                due_date TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    def close_connection(self):
        self.connection.close()