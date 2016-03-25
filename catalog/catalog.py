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
    list = [
        {'title': 'Title1', 'content': 'Content1', 'linka': 'Link1 A', 'linkb': 'Link1 B'},
        {'title': 'Title2', 'content': 'Content2', 'linka': 'Link2 A', 'linkb': 'Link2 B'},
        {'title': 'Title3', 'content': 'Content3', 'linka': 'Link3 A', 'linkb': 'Link3 B'},
        {'title': 'Title4', 'content': 'Content4', 'linka': 'Link4 A', 'linkb': 'Link4 B'},
        {'title': 'Title5', 'content': 'Content5', 'linka': 'Link5 A', 'linkb': 'Link5 B'},
    ]
    return render_template('index.html', cards=list)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        db.create_all()
    app.debug = True
    app.run(host='0.0.0.0')
