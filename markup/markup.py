# from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from settings import config
from data_base.dbalchemy import DBManager


class Keyboards:
    def __init__(self):
        self.markup = None
        self.DB = DBManager()

    def set_btn(self, name, step=0, quantity=0, message=None):
        if name == 'AMOUNT_ORDERS':
            config.KEYBOARD['AMOUNT_ORDERS'] = "{} {} {}".format(step + 1, ' из ',
                                                                 str(self.DB.count_rows_order(message.from_user.id)))
        if name == 'AMOUNT_PRODUCT':
            config.KEYBOARD['AMOUNT_PRODUCT'] = "{}".format(quantity)
        return KeyboardButton(config.KEYBOARD[name])

    def start_menu(self):
        self.markup = ReplyKeyboardMarkup(resize_keyboard=True)
        itm_btn_1 = self.set_btn('CHOOSE_GOODS')
        itm_btn_2 = self.set_btn('INFO')
        itm_btn_3 = self.set_btn('ORDER')
        itm_btn_4 = self.set_btn('SETTINGS')

        self.markup.row(itm_btn_1)
        self.markup.row(itm_btn_2, itm_btn_3, itm_btn_4)
        return self.markup

    def info_menu(self):
        self.markup = ReplyKeyboardMarkup(resize_keyboard=True)
        itm_btn_1 = self.set_btn('<<')
        self.markup.row(itm_btn_1)
        return self.markup

    def settings_menu(self):
        self.markup = ReplyKeyboardMarkup(resize_keyboard=True)
        itm_btn_1 = self.set_btn('<<')
        self.markup.row(itm_btn_1)
        return self.markup

    def category_menu(self, message=None):
        self.markup = ReplyKeyboardMarkup(resize_keyboard=True)
        itm_btn_1 = self.set_btn('CLOTH')
        itm_btn_2 = self.set_btn('FIGURINES')
        itm_btn_3 = self.set_btn('MUGS')
        self.markup.row(itm_btn_1)
        self.markup.row(itm_btn_2)
        self.markup.row(itm_btn_3)
        if message.from_user.id == config.ADMIN_ID:
            itm_btn_4 = self.set_btn('MAIN_MENU')
            self.markup.row(itm_btn_4)
        else:
            itm_btn_4 = self.set_btn('<<')
            itm_btn_5 = self.set_btn('ORDER')
            self.markup.row(itm_btn_4, itm_btn_5)
        return self.markup

    def payment_menu(self):
        self.markup = ReplyKeyboardMarkup(resize_keyboard=True)
        pay_btn = self.set_btn('APPLY')
        back_btn = self.set_btn('<<')
        self.markup.add(back_btn, pay_btn)
        return self.markup

    def orders_menu(self, step, quantity, message):
        self.markup = InlineKeyboardMarkup()
        down_btn = self.set_inline_btn('DOWN', 'down_count')
        amount_product_btn = self.set_inline_btn('AMOUNT_PRODUCT', 'amount_product', quantity=quantity)
        up_btn = self.set_inline_btn('UP', 'up_count')
        back_step_btn = self.set_inline_btn('BACK_STEP', 'back_product')
        amount_orders_btn = self.set_inline_btn('AMOUNT_ORDERS', 'amount_orders', step=step, message=message)
        next_step_btn = self.set_inline_btn('NEXT_STEP', 'next_product')
        delete_btn = self.set_inline_btn('X', 'delete_product_from_order')
        self.markup.add(down_btn, amount_product_btn, up_btn)
        self.markup.add(back_step_btn, amount_orders_btn, next_step_btn)
        self.markup.add(delete_btn)
        return self.markup

    def set_inline_btn(self, name, text, step=0, quantity=0, category='', message=None):
        if name == 'AMOUNT_ORDERS':
            config.KEYBOARD['AMOUNT_ORDERS'] = "{} {} {}".format(step + 1, ' из ',
                                                                 str(self.DB.count_rows_order(message.from_user.id)))
        if name == 'AMOUNT_PRODUCTS':
            config.KEYBOARD['AMOUNT_PRODUCTS'] = "{} {} {}".format(step + 1, ' из ',
                                                                   str(self.DB.count_rows_products_in_category(
                                                                       config.CATEGORY[category])))
        if name == 'AMOUNT_PRODUCT':
            config.KEYBOARD['AMOUNT_PRODUCT'] = "{}".format(quantity)
        return InlineKeyboardButton(config.KEYBOARD[name], callback_data=text)

    def set_select_category(self, category_id, left, right, page, pages_count):
        self.markup = InlineKeyboardMarkup()
        left_btn = self.set_inline_btn('BACK_STEP', f'to_{left}_{category_id}')
        page_btn = InlineKeyboardButton(f"{str(page + 1)}/{str(pages_count)}", callback_data='/')
        right_btn = self.set_inline_btn('NEXT_STEP', f'to_{right}_{category_id}')
        add_to_order_btn = self.set_inline_btn('ADD_TO_ORDER', f'add_{page}_{category_id}')
        self.markup.add(left_btn, page_btn, right_btn)
        self.markup.add(add_to_order_btn)
        return self.markup

    # Admin_Markup
    def start_admin_menu(self):
        self.markup = ReplyKeyboardMarkup(resize_keyboard=True)
        change_products_btn = self.set_btn('CHANGE_PRODUCTS')
        show_info_orders_btn = self.set_btn('SHOW_INFO_ORDERS')
        self.markup.add(change_products_btn)
        self.markup.add(show_info_orders_btn)
        return self.markup

    def change_menu_admin(self, step, quantity, category, product_id):
        self.markup = InlineKeyboardMarkup(row_width=3)
        down_btn = self.set_inline_btn('DOWN', f'down_product_count_{category}')
        amount_product_btn = self.set_inline_btn('AMOUNT_PRODUCT', 'amount_product', quantity=quantity)
        up_btn = self.set_inline_btn('UP', f'up_product_count_{category}')
        back_step_btn = self.set_inline_btn('BACK_STEP', f'back_product_{category}')
        amount_products_btn = self.set_inline_btn('AMOUNT_PRODUCTS', 'amount_products', step=step, category=category)
        next_step_btn = self.set_inline_btn('NEXT_STEP', f'next_product_{category}')
        change_btn = self.set_inline_btn('CHANGE', '_')
        rename_product_btn = self.set_inline_btn('CHANGE_NAME', f'change_name_{product_id}')
        change_price_btn = self.set_inline_btn('CHANGE_PRICE', f'change_price_{product_id}')
        change_photo_btn = self.set_inline_btn('CHANGE_PHOTO', f'change_image_{product_id}')
        delete_btn = self.set_inline_btn('X', f'delete_product_{product_id}_{category}')
        self.markup.add(down_btn, amount_product_btn, up_btn)
        self.markup.add(back_step_btn, amount_products_btn, next_step_btn)
        self.markup.add(change_btn)
        self.markup.add(rename_product_btn, change_price_btn, change_photo_btn)
        self.markup.add(delete_btn)
        return self.markup
