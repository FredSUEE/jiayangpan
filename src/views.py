from flask import (
    render_template,
    redirect,
    url_for
)
from flask_login import current_user
from src import app, db, login_manager
from .models import User


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(id))
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
@app.route('/index')
def index():
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
                           posts=posts)


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
