from models.product import Products
from models.user import Users
from sqlalchemy import Table, Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from data_base.dbcore import Base


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    data = Column(DateTime)
    product_id = Column(Integer, ForeignKey('products.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    products = relationship(Products, backref=backref('orders', uselist=True, cascade="delete,all"))
    users = relationship(Users, backref=backref('order', uselist=True, cascade="delete,all"))

    def __str__(self):
        return f"{self.quantity} {self.data}"
