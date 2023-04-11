from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from settings import config
from data_base.dbalchemy import DBManager


class Keyboards:
    def __init__(self):
        self.markup = None
        self.DB = DBManager()

    def set_btn(self, name, step = 0, quantity = 0, message = None):
        if name == 'AMOUNT_ORDERS':
            config.KEYBOARD['AMOUNT_ORDERS'] = "{} {} {}".format(step + 1, ' из ', str(self.DB.count_rows_order(message.from_user.id)))
        if name == 'AMOUNT_PRODUCT':
            config.KEYBOARD['AMOUNT_PRODUCT'] = "{}".format(quantity)
        return KeyboardButton(config.KEYBOARD[name])

    def start_menu(self):

        self.markup = ReplyKeyboardMarkup(True,True)
        itm_btn_1 = self.set_btn('CHOOSE_GOODS')
        itm_btn_2 = self.set_btn('INFO')
        itm_btn_3 = self.set_btn('SETTINGS')

        self.markup.row(itm_btn_1)
        self.markup.row(itm_btn_2, itm_btn_3)
        return self.markup

    def info_menu(self):

        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('<<')
        self.markup.row(itm_btn_1)
        return self.markup

    def settings_menu(self):
        self.markup = ReplyKeyboardMarkup(True,True)
        itm_btn_1 = self.set_btn('<<')
        self.markup.row(itm_btn_1)
        return self.markup

    def category_menu(self):
        self.markup = ReplyKeyboardMarkup(True,True)
        itm_btn_1 = self.set_btn('CLOTH')
        itm_btn_2= self.set_btn('FIGURINES')
        itm_btn_3=self.set_btn('MUGS')
        itm_btn_4=self.set_btn('<<')
        itm_btn_5=self.set_btn('ORDER')
        self.markup.row(itm_btn_1)
        self.markup.row(itm_btn_2)
        self.markup.row(itm_btn_3)
        self.markup.row(itm_btn_4,itm_btn_5)
        return self.markup
    def orders_menu(self, step, quantity, message):
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1=self.set_btn('X', step, quantity)
        itm_btn_2=self.set_btn('DOWN', step, quantity)
        itm_btn_3=self.set_btn('AMOUNT_PRODUCT', step, quantity)
        itm_btn_4=self.set_btn('UP', step, quantity)
        itm_btn_5=self.set_btn('BACK_STEP', step, quantity)
        itm_btn_6=self.set_btn('AMOUNT_ORDERS', step, quantity, message)
        itm_btn_7=self.set_btn('NEXT_STEP', step, quantity)
        itm_btn_8=self.set_btn('APPLY', step, quantity)
        itm_btn_9 = self.set_btn('<<', step, quantity)
        self.markup.row(itm_btn_2, itm_btn_3, itm_btn_4)
        self.markup.row(itm_btn_5, itm_btn_6, itm_btn_7)
        self. markup.row(itm_btn_9, itm_btn_1, itm_btn_8)
        return self.markup

    def set_inline_btn(self, name):
        return InlineKeyboardButton(str(name), callback_data=str(name.id))

    def set_select_category(self,category):
        self.markup = InlineKeyboardMarkup(row_width=1)
        for itm in self.DB.select_all_products_category(category):
            self.markup.add(self.set_inline_btn(itm))
        return self.markup