import tkinter as tk
from model.task import TaskModel
from model.database import Database as model
import sqlite3
from datetime import datetime
from tkinter import messagebox

class TaskView:
    def __init__(self, master, model):
        self.master = master
        self.master.title('Task Manager')

        self.model = model

        self.time_frame = tk.Frame(self.master, bd=2, relief=tk.RIDGE)
        self.time_frame.pack(pady=10)

        self.current_time_label = tk.Label(self.time_frame, text="", font=("Times New Roman", 12))
        self.current_time_label.pack()

        self.update_time()

        self.task_entry = tk.Entry(self.master, width=80)
        self.task_entry.pack(pady=10)

        self.tasks = []
        self.completed_tasks = []

        self.due_date_entry = tk.Entry(self.master, width=15)
        self.due_date_entry.pack(pady=5)
        self.due_date_entry.insert(0, 'YYYY-MM-DD HH:MM')

        self.task_entry.bind("<FocusIn>", self.clear_placeholder)
        self.due_date_entry.bind("<FocusIn>", self.clear_placeholder)


        self.add_task_button = tk.Button(self.master, text='Add task', width=25)
        self.add_task_button.pack()
        self.mark_as_completed_button = tk.Button(self.master, text='Mark as completed', width=25)
        self.mark_as_completed_button.pack()
        self.delete_task_button = tk.Button(self.master, text='Delete task', width=25)
        self.delete_task_button.pack()

        tk.Label(self.master, text="Tasks:").pack()
        self.task_listbox = tk.Listbox(self.master, width=50, selectmode=tk.SINGLE)
        self.task_listbox.pack(pady=10)

        tk.Label(self.master, text="Completed Tasks:").pack()
        self.completed_task_listbox = tk.Listbox(self.master, width=50, selectmode=tk.SINGLE)
        self.completed_task_listbox.pack(pady=10)

        self.update_task_list(self.model.get_tasks())
        self.update_completed_task_list(self.model.get_completed_tasks())

    def show_error(self, message):
        tk.messagebox.showerror("Error", message)

    def update_task_list(self, tasks):
        self.task_listbox.delete(0, tk.END)
        for task, due_date in tasks:
            self.task_listbox.insert(tk.END, f"{task} (Due: {due_date})")

    def update_completed_task_list(self, tasks):
        self.completed_task_listbox.delete(0, tk.END)
        for task, due_date in tasks:
            self.completed_task_listbox.insert(tk.END, f"{task} (Due: {due_date})")

    def set_add_task_command(self, command):
        self.add_task_button.config(command=command)

    def set_delete_task_command(self, command):
        self.delete_task_button.config(command=command)

    def set_mark_as_completed_command(self,command):
        self.mark_as_completed_button.config(command=command)

    def clear_placeholder(self, event):
        if event.widget.get() in ('Task', 'YYYY-MM-DD HH:MM'):
            event.widget.delete(0, tk.END)

    def update_time(self):
        current_time = datetime.now()
        current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        self.current_time_label.config(text=f"Current Time: {current_time_str}")
        self.master.after(1000, self.update_time)