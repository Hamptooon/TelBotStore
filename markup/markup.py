# from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from settings import config
from data_base.dbalchemy import DBManager


class Keyboards:
    def __init__(self):
        self.markup = None
        self.DB = DBManager()

    def set_btn(self, name, step=0, quantity=0, user_id=0):
        if name == 'AMOUNT_ORDERS':
            config.KEYBOARD['AMOUNT_ORDERS'] = "{} {} {}".format(step + 1, ' из ',
                                                                 str(self.DB.count_rows_order(user_id)))
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

    def category_menu(self, user_id=0):
        self.markup = ReplyKeyboardMarkup(resize_keyboard=True)
        itm_btn_1 = self.set_btn('CLOTH')
        itm_btn_2 = self.set_btn('FIGURINES')
        itm_btn_3 = self.set_btn('MUGS')
        self.markup.row(itm_btn_1)
        self.markup.row(itm_btn_2)
        self.markup.row(itm_btn_3)
        itm_btn_4 = self.set_btn('<<')
        if user_id != config.ADMIN_ID:
            itm_btn_5 = self.set_btn('ORDER')
            self.markup.row(itm_btn_4,itm_btn_5)
        else:
            self.markup.row(itm_btn_4)
        return self.markup

    def payment_menu(self):
        self.markup = ReplyKeyboardMarkup(resize_keyboard=True)
        pay_btn = self.set_btn('APPLY')
        back_btn = self.set_btn('<<')
        self.markup.add(back_btn, pay_btn)
        return self.markup

    def orders_menu(self, index, quantity, user_id):
        self.markup = InlineKeyboardMarkup()
        down_btn = self.set_inline_btn('DOWN', f'change_order_down_count_{index}_{user_id}')
        amount_product_btn = self.set_inline_btn('AMOUNT_PRODUCT', 'amount_product', quantity=quantity)
        up_btn = self.set_inline_btn('UP', f'change_order_up_count_{index}_{user_id}')
        back_step_btn = self.set_inline_btn('BACK_STEP', f'change_order_back_product_{index - 1}_{user_id}')
        amount_orders_btn = self.set_inline_btn('AMOUNT_ORDERS', 'amount_orders', step=index, user_id=user_id)
        next_step_btn = self.set_inline_btn('NEXT_STEP', f'change_order_next_product_{index + 1}_{user_id}')
        delete_btn = self.set_inline_btn('X', f'change_order_delete_product_{index}_{user_id}')
        self.markup.add(down_btn, amount_product_btn, up_btn)
        self.markup.add(back_step_btn, amount_orders_btn, next_step_btn)
        self.markup.add(delete_btn)
        return self.markup

    def set_inline_btn(self, name, text,current_user = 0, count_users = 0,  step=0, quantity=0, category='', user_id=0):
        if name == 'AMOUNT_ORDERS':
            config.KEYBOARD['AMOUNT_ORDERS'] = "{} {} {}".format(step + 1, ' из ',
                                                                 str(self.DB.count_rows_order(user_id)))
        elif name == 'AMOUNT_PRODUCTS':
            config.KEYBOARD['AMOUNT_PRODUCTS'] = "{} {} {}".format(step + 1, ' из ',
                                                                   str(self.DB.count_rows_products_in_category(
                                                                       config.CATEGORY[category])))
        elif name == 'AMOUNT_PRODUCT':
            config.KEYBOARD['AMOUNT_PRODUCT'] = "{}".format(quantity)

        elif name == 'AMOUNT_USERS':
            config.KEYBOARD['AMOUNT_USERS'] = "{} {} {}".format(current_user + 1, ' из ', count_users)
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
        add_product_btn = self.set_inline_btn('ADD_PRODUCT', f'add_product_{category}')
        delete_btn = self.set_inline_btn('X', f'delete_product_{product_id}_{category}')
        self.markup.add(down_btn, amount_product_btn, up_btn)
        self.markup.add(back_step_btn, amount_products_btn, next_step_btn)
        self.markup.add(change_btn)
        self.markup.add(rename_product_btn, change_price_btn, change_photo_btn)
        self.markup.add(add_product_btn)
        self.markup.add(delete_btn)
        return self.markup

    def users_info_menu_admin(self, current_page, count_users):
        self.markup = InlineKeyboardMarkup()
        back_user_btn = self.set_inline_btn('BACK_STEP', f'back_user_{current_page - 1}')
        next_user_btn = self.set_inline_btn('NEXT_STEP', f'next_user_{current_page + 1}')
        amount_users = self.set_inline_btn('AMOUNT_USERS', f'amount_users', current_user=current_page, count_users=count_users)
        choose_user_btn = self.set_inline_btn('CHOOSE_USER', 'choose_user_' + str(self.DB.select_user_from_info_users(current_page)))
        search_user_by_id_btn = self.set_inline_btn('SEARCH_USER', 'search_user')
        self.markup.add(back_user_btn, amount_users, next_user_btn)
        self.markup.add(choose_user_btn)
        self.markup.add(search_user_by_id_btn)
        return self.markup
    def user_order_menu_admin(self, current_page, count_products, quantity_product, user_id):
        self.markup = InlineKeyboardMarkup()
        down_btn = self.set_inline_btn('DOWN', 'down_user_product_count')
        amount_product_btn = self.set_inline_btn('AMOUNT_PRODUCT', 'amount_product', quantity=quantity_product)
        up_btn = self.set_inline_btn('UP', 'up_user_product_count')
        back_step_btn = self.set_inline_btn('BACK_STEP', 'back_user_product_')
        amount_orders_btn = self.set_inline_btn('AMOUNT_ORDERS', 'amount_orders', step=current_page, user_id=user_id)
        next_step_btn = self.set_inline_btn('NEXT_STEP', 'next_user_product_')
        delete_btn = self.set_inline_btn('X', f'delete_product_from_user_order_{current_page}_{user_id}')
        add_product_btn = self.set_inline_btn('ADD_TO_ORDER', 'add_product_in_user_order')
        self.markup.add(down_btn, amount_product_btn, up_btn)
        self.markup.add(back_step_btn, amount_orders_btn, next_step_btn)
        self.markup.add(delete_btn, add_product_btn)
        return self.markup

