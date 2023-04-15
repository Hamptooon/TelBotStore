from sqlalchemy import Table, Column,Text, String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
# from sqlalchemy.ext.declarative import declarative_base
from models.category import Category
# Base = declarative_base()
from data_base.dbcore import Base


class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    price = Column(Float)
    quantity = Column(Integer)
    is_active= Column(Boolean)
    category_id=Column(Integer, ForeignKey('category.id'))
    img_path = Column(Text)
    category = relationship(Category, backref=backref('products', uselist=True, cascade='delete,all'))


    def __str__(self):
        return f"{self.name} {self.price}"
