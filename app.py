import datetime

from cs50 import SQL
from flask import Flask, redirect, render_template, request, url_for

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///todo.db")

#homepage that shows all todos
@app.route('/')
def index():
    tasks = []
    rows = db.execute("SELECT * FROM tasks")
    if rows:
        for row in rows:
            tasks.append(row['name_of_task'])
        return render_template('index.html', tasks=tasks)
    else:
        return render_template('index.html')


@app.route('/', methods=["POST"])
#function to add a todo to db
def add():
    if request.method == "POST":
        task = request.form.get("task")
        if task:
            #insert tasks into todo table
            date = datetime.datetime.now()
            params = (task, date.strftime('%Y-%m-%d %H:%M:%S'))
            rows = db.execute("INSERT INTO 'tasks' ('name_of_task', 'date') VALUES (?, ?)", params)
            return redirect("/")
        else:
            return render_template("index.html")


@app.route('/delete/<string:name_of_task>')
#function to delete a todo from db
def delete(name_of_task):
    if not name_of_task:
        return redirect('/')
    else:
        rows = db.execute("DELETE FROM tasks WHERE name_of_task = :name_of_task", name_of_task=name_of_task)
        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)