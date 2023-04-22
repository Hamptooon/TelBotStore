import os
import uuid
from datetime import datetime
from os import path
import io
from PIL import Image
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from data_base.dbcore import Base
from settings import config
from models.product import Products
from models.order import Order
from models.user import Users
from settings import utility


class Singleton(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, attrs, bases)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class DBManager(metaclass=Singleton):
    def __init__(self):
        self.engine = create_engine(config.DATABASE)
        session = sessionmaker(bind=self.engine)
        self._session = session()
        if not path.isfile(config.DATABASE):
            Base.metadata.create_all(self.engine)

    def select_all_products_category(self, category):
        result = self._session.query(Products).filter_by(category_id=category).all()
        self.close()
        return result

    def select_all_products_category_first(self, category):
        result = self.select_all_products_category(category)
        return result[0]

    def select_count_products_in_category(self, category):
        count = self._session.query(Products).filter_by(category_id=category).count()
        self.close()
        return count

    def select_all_products_id_in_category(self, category):
        products_id = self._session.query(Products.id).filter_by(category_id=category).all()
        self.close()
        return utility.convert(products_id)

    def close(self):
        self._session.close()

    def add_order(self, quantity, product_id, user_id):
        all_id_products = self.select_all_products_id_in_order_by_user(user_id)
        if product_id in all_id_products:
            quantity_order = self.select_quantity_product_in_order(product_id, user_id)
            quantity_order += 1
            self.update_order_value(product_id, user_id, 'quantity', quantity_order)
            quantity_product = self.select_single_product_quantity(product_id)
            quantity_product -= 1
            self.update_product_value(product_id, 'quantity', quantity_product)
            return
        else:
            order = Order(quantity=quantity, product_id=product_id, user_id=user_id, data=datetime.now())
            quantity_product = self.select_single_product_quantity(product_id)
            quantity_product -= 1
            self.update_product_value(product_id, 'quantity', quantity_product)
        self._session.add(order)
        self._session.commit()
        self.close()

    def select_all_products_id_in_order_by_user(self, user_id):
        result = self._session.query(Order.product_id).filter_by(user_id=user_id).all()
        self.close()
        return utility.convert(result)

    def select_quantity_product_in_order(self, product_id, user_id):
        result = self._session.query(Order.quantity).filter_by(product_id=product_id, user_id=user_id).one()
        self.close()
        return result.quantity

    def select_single_product_quantity(self, product_id):
        result = self._session.query(Products).filter_by(id=product_id).one()
        self.close()
        return result.quantity

    def select_single_product_name(self, product_id):
        result = self._session.query(Products).filter_by(id=product_id).one()
        self.close()
        return result.name

    def select_single_product_price(self, product_id):
        result = self._session.query(Products).filter_by(id=product_id).one()
        self.close()
        return result.price
    def select_single_product_image_path(self, product_id):
        result = self._session.query(Products).filter_by(id=product_id).one()
        self.close()
        return result.img_path
    def select_single_product_info(self, product_id):
        result = self._session.query(Products).filter_by(id=product_id).one()
        self.close()
        return result.name, result.price, result.quantity

    def select_single_product_info_in_shopping_cart(self, product_id, user_id):
        result = self._session.query(Products).filter_by(id=product_id).one()
        result_quantity = self._session.query(Order.quantity).filter_by(product_id=product_id, user_id=user_id).one()
        self.close()
        return result.name, result.price, result_quantity.quantity

    def select_single_product_img(self, product_id):
        result = self._session.query(Products).filter_by(id=product_id).one()
        self.close()
        return result.img_path

    def update_order_value(self, product_id, user_id, name, value):
        self._session.query(Order).filter_by(product_id=product_id, user_id=user_id).update({name: value})
        self._session.commit()
        self.close()

    def update_product_value(self, product_id, name, value):
        self._session.query(Products).filter_by(id=product_id).update({name: value})
        self._session.commit()
        self.close()

    def delete_order(self, product_id, user_id):
        self._session.query(Order).filter_by(product_id=product_id, user_id=user_id).delete()
        self._session.commit()
        self.close()
    def update_name_product(self, product_id, new_name):
        self._session.query(Products).filter_by(id=product_id).update({'name': new_name})
        self._session.commit()
        self.close()
    def update_price_product(self, product_id, new_price):
        self._session.query(Products).filter_by(id=product_id).update({'price': new_price})
        self._session.commit()
        self.close()
    def update_image_product(self, product_id, new_image):
        now = datetime.now()
        current_time = now.strftime("%Y_%m_%d_%H_%M_%S")
        product_name = self.select_single_product_name(product_id)
        format_product_name = product_name.replace(" ", "_").replace("/", "_")
        old_image_path = self.select_single_product_image_path(product_id)
        os.remove(old_image_path)
        image_name = f'{current_time}_{format_product_name}.jpg'
        image_path = 'media/' + image_name
        with open(image_path, 'wb') as image:
            image.write(new_image)

        self._session.query(Products).filter_by(id=product_id).update({'img_path': image_path})
        self._session.commit()
        self.close()
    def select_all_orders_id(self, user_id):
        result = self._session.query(Order.id).filter_by(user_id=user_id).all()
        self.close()
        return utility.convert(result)

    def delete_all_order(self, user_id):
        all_id_orders = self.select_all_orders_id(user_id)
        for itm in all_id_orders:
            self._session.query(Products).filter_by(id=itm).delete()
            self._session.commit()
        self.close()

    def delete_product(self, product_id):
        self._session.query(Products).filter_by(id=product_id).delete()
        # self._session.commit()
        # self.close()

    def count_rows_order(self, user_id):
        result = self._session.query(Order).filter_by(user_id=user_id).count()
        self.close()
        return result

    def count_rows_products_in_category(self, category):
        result = self._session.query(Products).filter_by(category_id=category).count()
        self.close()
        return result

    def check_order_present(self, user_id):
        if self.count_rows_order(user_id) == 0:
            return False
        else:
            return True

    def add_user_info(self, user_id, first_name, last_name, username):
        if not self.user_exists(user_id):
            new_user = Users(id=user_id, first_name=first_name, last_name=last_name, contact=username)
            self._session.add(new_user)
            self._session.commit()
            self.close()

    def select_user(self, user_id):
        user = self._session.query(Users).filter_by(id=user_id).one()
        self.close()
        return user

    def user_exists(self, user_id):
        try:
            self._session.query(Users).filter_by(id=user_id).one()
            self.close()
            return True
        except NoResultFound:
            return False

    def check_product_in_order(self, product_id):
        count_rows_product_in_order = self._session.query(Order).filter_by(product_id=product_id).count()
        self.close()
        if count_rows_product_in_order == 0:
            return False
        else:
            return True
