from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SelectField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    name = StringField('Task Name', validators=[DataRequired()])
    due_date = DateTimeField('Due Date', validators=[DataRequired()], format='%Y-%m-%d')
    priority_level = SelectField('Priority Level', validators=[DataRequired()],
                                 choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    status = SelectField('Status', validators=[DataRequired()],
                         choices=[('not_started', 'Not Started'), ('in_progress', 'In Progress'), ('completed', 'Completed')])
