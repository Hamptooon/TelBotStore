from sqlalchemy import Table, Column, Text, String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
# from sqlalchemy.ext.declarative import declarative_base
from models.category import Category
# Base = declarative_base()
from data_base.dbcore import Base


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    contact = Column(String)

    def __str__(self):
        return f"""
<b>👤 Сведения о клиенте:</b> #{self.id}
                
<b>Имя:{self.first_name}</b>
<b>Фамилия:{self.last_name}</b>
                
<b>☎️Контакты:{self.contact}</b>"""
