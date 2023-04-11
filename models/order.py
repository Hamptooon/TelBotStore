from models.product import Products
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column,Integer,DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
# Base = declarative_base()
from data_base.dbcore import Base


class Order(Base):

    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    data = Column(DateTime)
    product_id = Column(Integer, ForeignKey('products.id'))
    user_id = Column(Integer)
    products = relationship(Products, backref=backref('orders', uselist=True, cascade="delete,all"))

    def __str__(self):
        return f"{self.quantity} {self.data}"


