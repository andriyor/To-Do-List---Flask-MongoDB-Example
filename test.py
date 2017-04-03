from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'project1',
}
app.config['SECRET_KEY'] = 'hard to guess string'
db = MongoEngine(app)


class UserForm(FlaskForm):
    name = StringField('Task Name')
    desc = StringField('Description Name')
    date = DateField('Date', format="%m/%d/%Y")
    pr = SelectField(u'Priority', choices=[('1', '1'), ('2', '2'), ('3', '3')])
    submit = SubmitField('Отправить')


class User(db.Document):
    name = db.StringField()
    desc = db.StringField()
    date = db.DateTimeField()
    pr = db.StringField()
    done = db.StringField(default='no')


def redirect_url():
    return request.args.get('next') or request.referrer or url_for('index')


@app.route("/", methods=('GET', 'POST'))
def lists():
    form = UserForm(request.form)
    todos_l = User.objects
    a1 = "active"
    if request.method == 'POST':
        User(form.name.data, form.desc.data, form.date.data,
             form.pr.data).save()
    return render_template('index.html', a1=a1, todos=todos_l, form=form)


@app.route("/uncompleted")
def tasks():
    # Display the Uncompleted Tasks
    form = UserForm(request.form)
    todos_l = User.objects(done="no")
    a2 = "active"
    return render_template('index.html', a2=a2, todos=todos_l, form=form)


@app.route("/completed")
def completed():
    # Display the Completed Tasks
    form = UserForm(request.form)
    todos_l = User.objects(done="yes")
    a3 = "active"
    return render_template('index.html', a3=a3, todos=todos_l, form=form)


@app.route("/done")
def done():
    # Done-or-not ICON
    _id = request.values.get("_id")
    rem = User.objects.get(id=_id)
    if rem.done == 'yes':
        User.objects(id=_id).update(done='no')
    else:
        User.objects(id=_id).update(done='yes')
    return redirect(url_for('lists'))


@app.route("/remove")
def remove():
    # Deleting a Task with various references
    _id = request.values.get("_id")
    rem = User.objects.get(id=_id)
    rem.delete()
    return redirect("/")


@app.route("/update", methods=('GET', 'POST'))
def update():
    _id = request.values.get("_id")
    task = User.objects.get(id=_id)
    form = UserForm(request.form)
    if request.method == 'POST':
        _id = request.values.get("_id")
        print(_id)
        User.objects(id=_id).update(name=form.name.data, desc=form.desc.data, date=form.date.data, pr=form.pr.data)
        return redirect(url_for('lists'))
    return render_template('update.html', task=task, form=form)


@app.route("/search", methods=['GET'])
def search():
    # todo search
    pass


@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
