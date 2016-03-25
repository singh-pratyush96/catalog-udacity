import sys

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vagrant:123@localhost:5432/catalog'
db = SQLAlchemy(app)


# User model
class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_first_name = db.Column(db.String(30), nullable=False)
    user_last_name = db.Column(db.String(30), nullable=False)
    user_email = db.Column(db.String(120), unique=True)


# Category Model
class Category(db.Model):
    __tablename__ = "categories"

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(30), nullable=False)


# Item Model
class Item(db.Model):
    __tablename__ = "items"

    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    item_name = db.Column(db.String(30), nullable=False)
    item_description = db.Column(db.String(256))
    item_create_time = db.Column(db.DateTime)


@app.route('/')
def index():
    _list = [
        {'title': 'Title1'},
        {'title': 'Title2'},
        {'title': 'Title3'},
        {'title': 'Title4'},
        {'title': 'Title5'},
        {'title': 'Title6'},
        {'title': 'Title7'},
        {'title': 'Title8'},
        {'title': 'Title9'},
        {'title': 'Title0'},
    ]
    return render_template('index.html', categories=_list)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        db.create_all()
    app.debug = True
    app.run(host='0.0.0.0')
