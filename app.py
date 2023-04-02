from flask import Flask, render_template, redirect, url_for, request, flash
from forms import TaskForm
from models import db, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'

db.init_app(app)

def create_app():
    with app.app_context():
        db.create_all()

        return app

@app.route('/')
def index():
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'due_date')
    order = request.args.get('order', 'asc')

    query = Task.query

    if search:
        query = query.filter(Task.name.contains(search), Task.status.contains(search))

    if sort == 'due_date':
        query = query.order_by(Task.due_date.asc() if order == 'asc' else Task.due_date.desc())
    elif sort == 'priority_level':
        query = query.order_by(Task.priority_level.asc() if order == 'asc' else Task.priority_level.desc())
    elif sort == 'status':
        query = query.order_by(Task.status.asc() if order == 'asc' else Task.status.desc())

    tasks = query.all()

    return render_template('index.html', tasks=tasks, search=search, sort=sort, order=order)

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    form = TaskForm()

    if form.validate_on_submit():
        task = Task(name=form.name.data, due_date=form.due_date.data,
                    priority_level=form.priority_level.data, status=form.status.data)
        db.session.add(task)
        db.session.commit()
        
        return redirect(url_for('index'))

    return render_template('add_task.html', form=form)

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)

    if form.validate_on_submit():
        task.name = form.name.data
        task.due_date = form.due_date.data
        task.priority_level = form.priority_level.data
        task.status = form.status.data
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_task.html', form=form)

@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/task_stats')
def task_stats():
    not_started_count = Task.query.filter_by(status='not_started').count()
    in_progress_count = Task.query.filter_by(status='in_progress').count()
    completed_count = Task.query.filter_by(status='completed').count()

    low_priority_count = Task.query.filter_by(priority_level='low').count()
    medium_priority_count = Task.query.filter_by(priority_level='medium').count()
    high_priority_count = Task.query.filter_by(priority_level='high').count()

    return render_template('task_stats.html', not_started_count=not_started_count,
                           in_progress_count=in_progress_count, completed_count=completed_count,
                           low_priority_count=low_priority_count, medium_priority_count=medium_priority_count,
                           high_priority_count=high_priority_count)

create_app()

if __name__ == '__main__':
    app.run(debug=True)
