from app import *
from flask import render_template, redirect, session, url_for, flash
from datetime import datetime
from .forms import *
@app.route('/')
@app.route('/index')
def index():
    #print(datetime.utcnow())
    return render_template("index.html", current_time=datetime.now())

@app.route('/formtest', methods=['GET', 'POST'])
def formtest():
    #print(datetime.utcnow())
    #name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        #if old_name is not None and old_name != form.name.data:
           # print("---------------------------")
        flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        form.name.data = ''
        #return redirect(url_for("formtest",name=session.get('name')))
    return render_template("formtest.html", form=form, name=session.get('name'))

@app.route('/hello/<name>')
def hello(name):
    print("session['name']:", session)
    return render_template("hello.html", name=name)