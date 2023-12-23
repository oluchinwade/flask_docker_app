from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, server_default="1")
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True,nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)

    def __init__(self,username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email
    # converting object to JSON format
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email              
        }


class Vendor(db.Model):
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, server_default="1")
    name = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    products = db.relationship('Product', backref='vendor', lazy=True)
    def __init__(self, name:str, email:str):
        self.name = name
        self.email = email

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email              
        }

product_order = db.Table(
    'product_order',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
    db.Column('date_time',db.DateTime, default=datetime.datetime.utcnow, nullable=False),
    db.Column('amount', db.Float, nullable=False)
)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, server_default="1")
    amount =  db.Column(db.Numeric, nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    orders_with_product = db.relationship('Product', secondary=product_order, backref='order', lazy=True)
    def __init__(self, amount:int, user_id:int):
        self.amount = amount
        self.user_id = user_id

    def serialize(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'user_id': self.user_id,
            'date_time': self.date_time.isoformat()             
        }


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, server_default="1")
    name = db.Column(db.String(128), unique=True, nullable=False) 
    category = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(280), nullable=False)
    amount = db.Column(db.Numeric, nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    def __init__(self, name:str, category:str, description:str, amount:int, vendor_id:int):
        self.name = name
        self.category = category
        self.description = description
        self.amount = amount
        self.vendor_id = vendor_id

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'amount': self.amount,
            'vendor_id': self.vendor_id           
        }
