import tkinter as tk
from datetime import datetime


class TaskManagerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title('Task Manager')

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

    def clearPlaceholder(self, event):
        if event.widget.get() in ('Task', 'YYYY-MM-DD HH:MM'):
            event.widget.delete(0, tk.END)

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
            except ValueError:
                print('Invalid date format. Please use YYYY-MM-DD HH:MM.')

    def deleteTask(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task, due_date = self.tasks.pop(selected_index[0])
            self.task_listbox.delete(selected_index)
            print(f'Task "{task}" (Due: {due_date.strftime("%Y-%m-%d %H:%M")}) removed.')

    def updateTime(self):
        current_time = datetime.now()
        current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        self.current_time_label.config(text=f"Current Time: {current_time_str}")
        for task, due_date in self.tasks:
            if due_date < current_time:
                task_with_time = f'{task} (Due: {due_date.strftime("%Y-%m-%d %H:%M")})'
                index = self.tasks.index((task, due_date))
                self.task_listbox.itemconfig(index, {'bg': 'red'})
            else:
                task_with_time = f'{task} (Due: {due_date.strftime("%Y-%m-%d %H:%M")})'
                index = self.tasks.index((task, due_date))
                self.task_listbox.itemconfig(index, {'bg': 'white'})

        self.master.after(1000, self.update_time)

    def markAsCompleted(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task, due_date = self.tasks.pop(selected_index[0])
            task_with_time = f'{task} (Due: {due_date.strftime("%Y-%m-%d %H:%M")})'
            self.tasks.append((task, due_date))
            self.completed_task_listbox.insert(tk.END, task_with_time)
            self.task_listbox.delete(selected_index)
            self.completed_task_listbox.itemconfig(selected_index, {'bg': 'green'})


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()
