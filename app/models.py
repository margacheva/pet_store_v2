from flask_login import UserMixin
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from app import db


engine = create_engine('postgresql+psycopg2://yana:yana@localhost:44444/postgres')
Base = declarative_base()


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)


class Poop(db.Model):
    __tablename__ = 'poop'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    photo = db.Column(db.String, nullable=False)


class CartItem(db.Model):
    __tablename__ = 'cart_item'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('poop.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    subtotal = db.Column(db.Float, default=0.0, nullable=False)
    product = db.relationship('Poop', backref='cart_items')

    def update_total_price(self):
        self.subtotal = self.quantity * self.product.price
