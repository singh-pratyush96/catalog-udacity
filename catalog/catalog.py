from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/catalog'
db = SQLAlchemy(app)


# User model
class User(db.Model):
    __table_name__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    user_first_name = db.Column(db.String(30), nullable=False)
    user_last_name = db.Column(db.String(30), nullable=False)
    user_email = db.Column(db.String(120), unique=True)


# Category Model
class Catrgory(db.Model):
    __table_name__ = "categories"

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(30), nullable=False)


# Items Model
class Items(db.Model):
    __table_name__ = "items"

    item_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.cotegoty_id'))
    item_name = db.Column(db.String(30), nullable=False)
    item_description = db.Column(db.String(256))
    item_create_time = db.Column(db.DateTime)