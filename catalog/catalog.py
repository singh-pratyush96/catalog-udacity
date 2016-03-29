import json

from flask import Flask, render_template, request
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
    category_description = db.Column(db.String(300), nullable=False)

    def __init__(self, category_name, category_description):
        self.category_name = category_name
        self.category_description = category_description

    def serialize(self):
        _dict = {
            'category_id': self.category_id,
            'category_name': self.category_name
        }
        return _dict


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
    categories = Category.query.all()
    _list = [Category.serialize(x) for x in categories]

    return render_template('index.html', categories=_list)


@app.route('/category/create')
def create_category_page():
    return render_template('create_category.html')


@app.route('/category/create', methods=['POST'])
def create_category():
    category_name = request.form['category_name']
    category_description = request.form['category_description']

    if len(Category.query.filter_by(category_name=category_name).all()) != 0:
        status = '1'
    else:
        db.session.add(Category(category_name, category_description))
        db.session.commit()
        status = '0'

    _dict = {
        "status": status,
        "category_name": category_name,
        "category_description": category_description
    }
    return json.dumps(_dict)


@app.route('/category/<int:category_id>/')
def static_page_category(category_id):
    content = Category.query.filter_by(category_id=category_id).first()
    items = Item.query.filter(Item.category_id == content.category_id)

    _dict = {
        "category_id": content.category_id,
        "category_name": content.category_name,
        "category_description": content.category_description,
        "number_of_items": len([x for x in items]),
        "items": items
    }

    return render_template('category.html', content=_dict)


@app.route('/item/<int:item_id>')
def static_page_item(item_id):
    item = Item.query.filter_by(item_id=item_id).first()
    category = Category.query.filter_by(category_id=item.category_id).first()
    user = User.query.filter_by(user_id=item.user_id).first()
    content = {
        'item': item,
        'category': category,
        'user': user
    }
    return render_template('item.html', content=content)


if __name__ == "__main__":
    db.create_all()
    app.debug = True
    app.run(host='0.0.0.0')