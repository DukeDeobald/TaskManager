# TaskManager

My first project - a Task Manager with basic functionality. In current version it is possible to:
1. Add task to the list (Note: time should be inputted as YYYY-MM-DD HH:MM, where you have to input '-' and ':' by yourself, otherwise you will get an error)
2. Delete task from the list
3. Mark task as completed (Moves it to "completed tasks" and colours it green)
4. If due time for the task expired it will be coloured red.

   There are some known issues related to the task with very long name, errors not showing up, tasks not being saved after closing the application and the need to input time in right format all by yourself.
   
   I will be updating this product as long as possible so stay tuned.

# Installation

1. Clone a repo ``git clone https://github.com/DukeDeobald/TaskManager``

2. Create Python virtual environment ``python3 -m venv .venv``

3. Activate virtual env ``source .venv/bin/activate``

4. Run it using ``python3 main.py``
