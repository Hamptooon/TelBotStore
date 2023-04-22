from sqlalchemy import Column, String, Integer
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
