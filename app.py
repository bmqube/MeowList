from flask import Flask, render_template, url_for, redirect, flash, get_flashed_messages
from forms import NotunForm, DeleteForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db = SQLAlchemy(app)

from models import Task

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = NotunForm()
    if form.validate_on_submit():
        t = Task(title=form.name.data, date=datetime.utcnow())
        db.session.add(t)
        db.session.commit()
        flash('Task added to the database')
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    task = Task.query.get(task_id)
    form = NotunForm()
    if task:
        if form.validate_on_submit():
            task.title = form.name.data
            task.date = datetime.utcnow()
            db.session.commit()
            flash("Task has been updated")
            return redirect(url_for('index'))
        form.name.data = task.title
        return render_template('edit.html', form=form, task_id=task_id)
    flash("Task not found")
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['GET', 'POST'])
def delete(task_id):
    task = Task.query.get(task_id)
    form = DeleteForm()
    if task:
        if form.validate_on_submit():
            db.session.delete(task)
            db.session.commit()
            flash("Task has been deleted")
            return redirect(url_for('index'))
        return render_template('delete.html', form=form, title=task.title, task_id=task_id)
    flash("Task not found")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)
