import tkinter as tk
from datetime import datetime
import sqlite3


class TaskManagerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title('Task Manager')

        self.connection = sqlite3.connect("taskManager.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                due_date TEXT NOT NULL
            )
        ''')

        self.connection.commit()

        self.tasks = []

        self.time_frame = tk.Frame(self.master, bd=2, relief=tk.RIDGE)
        self.time_frame.pack(pady=10)

        self.current_time_label = tk.Label(self.time_frame, text="", font=("Times New Roman", 12))
        self.current_time_label.pack()

        self.updateTime()

        self.task_entry = tk.Entry(self.master, width=80)
        self.task_entry.pack(pady=10)

        self.due_date_entry = tk.Entry(self.master, width=15)
        self.due_date_entry.pack(pady=5)
        self.due_date_entry.insert(0, 'YYYY-MM-DD HH:MM')

        self.task_entry.bind("<FocusIn>", self.clearPlaceholder)
        self.due_date_entry.bind("<FocusIn>", self.clearPlaceholder)

        button = tk.Button(self.master, text='Add task', width=25, command=self.addTask)
        button.pack()
        button = tk.Button(self.master, text='Mark as completed', width=25, command=self.markAsCompleted)
        button.pack()
        button = tk.Button(self.master, text='Delete task', width=25, command=self.deleteTask)
        button.pack()

        tk.Label(self.master, text="Tasks:").pack()
        self.task_listbox = tk.Listbox(self.master, width=50, selectmode=tk.SINGLE)
        self.task_listbox.pack(pady=10)

        tk.Label(self.master, text="Completed Tasks:").pack()
        self.completed_task_listbox = tk.Listbox(self.master, width=50, selectmode=tk.SINGLE)
        self.completed_task_listbox.pack(pady=10)

        self.load_tasks_from_db()

        self.master.protocol("WM_DELETE_WINDOW", self.close_db)

    def clearPlaceholder(self, event):
        if event.widget.get() in ('Task', 'YYYY-MM-DD HH:MM'):
            event.widget.delete(0, tk.END)
        pass

    def addTask(self):
        task = self.task_entry.get()
        due_date_str = self.due_date_entry.get()

        if task and due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d %H:%M')
                task_with_time = f'{task} (Due: {due_date.strftime("%Y-%m-%d %H:%M")})'
                self.tasks.append((task, due_date))
                self.task_listbox.insert(tk.END, task_with_time)
                self.task_entry.delete(0, tk.END)
                self.due_date_entry.delete(0, tk.END)
                self.save_task_to_db(task, due_date_str)
            except ValueError:
                print('Invalid date format. Please use YYYY-MM-DD HH:MM.')
        pass

    def deleteTask(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task, due_date = self.tasks.pop(selected_index[0])
            self.task_listbox.delete(selected_index)
            print(f'Task "{task}" (Due: {due_date.strftime("%Y-%m-%d %H:%M")}) removed.')
            self.remove_task_from_db(task, due_date.strftime('%Y-%m-%d %H:%M'))
        pass

    def updateTime(self):
        current_time = datetime.now()
        current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        self.current_time_label.config(text=f"Current Time: {current_time_str}")
        for task, due_date in self.tasks:
            if due_date < current_time:
                index = self.tasks.index((task, due_date))
                self.task_listbox.itemconfig(index, {'bg': 'red'})
            else:
                pass

        self.master.after(1000, self.updateTime)

    def save_task_to_db(self, task, due_date):
        self.cursor.execute("INSERT INTO tasks (task, due_date) VALUES (?, ?)", (task, due_date))
        self.connection.commit()

    def load_tasks_from_db(self):
        self.cursor.execute("SELECT task, due_date FROM tasks")
        rows = self.cursor.fetchall()
        for row in rows:
            task = row[0]
            due_date_str = row[1]
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d %H:%M')
            task_with_time = f'{task} (Due: {due_date.strftime("%Y-%m-%d %H:%M")})'
            self.tasks.append((task, due_date))
            self.task_listbox.insert(tk.END, task_with_time)

    def remove_task_from_db(self, task, due_date):
        self.cursor.execute("DELETE FROM tasks WHERE task = ? AND due_date = ?", (task, due_date))
        self.connection.commit()

    def close_db(self):
        self.connection.close()
        self.master.destroy()

    def markAsCompleted(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task, due_date = self.tasks.pop(selected_index[0])
            task_with_time = f'{task} (Due: {due_date.strftime("%Y-%m-%d %H:%M")})'
            self.tasks.append((task, due_date))
            self.completed_task_listbox.insert(tk.END, task_with_time)
            self.task_listbox.delete(selected_index)
            self.completed_task_listbox.itemconfig(selected_index, {'bg': 'green'})
            self.remove_task_from_db(task, due_date.strftime('%Y-%m-%d %H:%M'))
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()
