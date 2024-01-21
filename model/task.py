from .database import Database
import sqlite3

class TaskModel:
    def __init__(self, database: Database):
        self.database = database

    def add_task(self, task, due_date):
        try:
            self.database.cursor.execute("INSERT INTO tasks (task, due_date) VALUES (?, ?)", (task, due_date))
            self.database.connection.commit()
        except sqlite3.Error as e:
            print(f"Error adding task: {e}")
            self.database.connection.rollback()


    def delete_task(self, task, due_date):
        try:
            task_name = task.split(" (Due:")[0].strip()
            self.database.cursor.execute("DELETE FROM tasks WHERE task = ? AND due_date = ?", (task, due_date))
            self.database.cursor.execute("DELETE FROM completed_tasks WHERE task = ? AND due_date = ?", (task, due_date))
            self.database.connection.commit()
        except sqlite3.Error as e:
            print(f"Error deleting task: {e}")
            self.database.connection.rollback()

    def get_tasks(self):
        try:
            self.database.cursor.execute("SELECT task, due_date FROM tasks")
            return self.database.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting tasks: {e}")
            self.database.connection.rollback()

    def get_completed_tasks(self):
        try:
            self.database.cursor.execute("SELECT task, due_date FROM completed_tasks")
            return self.database.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting tasks: {e}")
            self.database.connection.rollback()

    def mark_task_as_completed(self, task, due_date):
        try:
            self.delete_task(task, due_date)
            self.database.cursor.execute("INSERT INTO completed_tasks (task, due_date) VALUES (?, ?)", (task, due_date))
            self.database.connection.commit()
        except sqlite3.Error as e:
            print(f"Error marking task as completed: {e}")
            self.database.connection.rollback()
