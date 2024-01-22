from view.task_view import TaskView
from model.task import TaskModel
import sqlite3

class TaskController:
    def __init__(self, view: TaskView, model: TaskModel):
        self.view = view
        self.model = model
        self.view.set_add_task_command(self.add_task)
        self.view.set_mark_as_completed_command(self.mark_as_completed)
        self.view.set_delete_task_command(self.delete_task)

    def add_task(self):
        task = self.view.task_entry.get()
        due_date = self.view.due_date_entry.get()

        self.view.update_task_list(self.model.get_tasks())
        self.model.add_task(task, due_date)


    def delete_task(self):
        selected_index = self.view.task_listbox.curselection()
        if selected_index:
            selected_task = self.view.task_listbox.get(selected_index[0])
            task_name = selected_task.split(" (Due:")[0].strip()
            due_date = selected_task.split(" (Due:")[1].split(")")[0].strip()
            try:
                self.model.delete_task(task_name, due_date)
                self.view.update_task_list(self.model.get_tasks())
                self.view.update_completed_task_list(self.model.get_completed_tasks())
            except sqlite3.Error as e:
                print(f"Error deleting task: {e}")
        selected_index = self.view.completed_task_listbox.curselection()
        if selected_index:
            selected_task = self.view.completed_task_listbox.get(selected_index[0])
            task_name = selected_task.split(" (Due:")[0].strip()
            due_date = selected_task.split(" (Due:")[1].split(")")[0].strip()
            try:
                self.model.delete_task(task_name, due_date)
                self.view.update_task_list(self.model.get_tasks())
                self.view.update_completed_task_list(self.model.get_completed_tasks())
            except sqlite3.Error as e:
                print(f"Error deleting completed task: {e}")

    def mark_as_completed(self):
        selected_index = self.view.task_listbox.curselection()
        if selected_index:
            try:
                selected_task = self.view.task_listbox.get(selected_index[0])
                task_name = selected_task.split(" (Due:")[0].strip()
                due_date = selected_task.split(" (Due:")[1].split(")")[0].strip()
                self.model.mark_task_as_completed(task_name, due_date)
                self.view.update_task_list(self.model.get_tasks())
                self.view.update_completed_task_list(self.model.get_completed_tasks())
                self.view.completed_task_listbox.itemconfig(selected_index, {'bg': 'green'})
            except sqlite3.Error as e:
                print(f"Error marking task as completed: {e}")