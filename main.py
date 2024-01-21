import tkinter as tk
from model.database import Database
from model.task import TaskModel
from view.task_view import TaskView
from controller.task_controller import TaskController

def main():
    root = tk.Tk()
    database = Database("taskManager.db")
    model = TaskModel(database)
    view = TaskView(root, model)
    controller = TaskController(view, model)
    root.mainloop()

if __name__ == "__main__":
    main()