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
        itm_btn_3 = self.set_btn('ORDER')
        itm_btn_4 = self.set_btn('SETTINGS')

        self.markup.row(itm_btn_1)
        self.markup.row(itm_btn_2, itm_btn_3, itm_btn_4)
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
    def payment_menu(self):
        self.markup = ReplyKeyboardMarkup(True, True)
        pay_btn = self.set_btn('APPLY')
        back_btn = self.set_btn('<<')
        self.markup.add(back_btn,pay_btn)
        return self.markup
    def orders_menu(self, step, quantity, message):
        self.markup = InlineKeyboardMarkup()
        down_btn = self.set_inline_btn('DOWN', 'down_count')
        amount_product_btn = self.set_inline_btn('AMOUNT_PRODUCT', 'amount_product', quantity=quantity)
        up_btn = self.set_inline_btn('UP', 'up_count')
        back_step_btn = self.set_inline_btn('BACK_STEP', 'back_product')
        amount_orders_btn = self.set_inline_btn('AMOUNT_ORDERS', 'amount_orders', step=step, message=message)
        next_step_btn = self.set_inline_btn('NEXT_STEP', 'next_product')
        delete_btn = self.set_inline_btn('X', 'delete_product')
        self.markup.add(down_btn, amount_product_btn, up_btn)
        self.markup.add(back_step_btn, amount_orders_btn, next_step_btn)
        self.markup.add(delete_btn)
        return self.markup
        # self.markup = ReplyKeyboardMarkup(True, True)
        # itm_btn_1=self.set_btn('X', step, quantity)
        # itm_btn_2=self.set_btn('DOWN', step, quantity)
        # itm_btn_3=self.set_btn('AMOUNT_PRODUCT', step, quantity)
        # itm_btn_4=self.set_btn('UP', step, quantity)
        # itm_btn_5=self.set_btn('BACK_STEP', step, quantity)
        # itm_btn_6=self.set_btn('AMOUNT_ORDERS', step, quantity, message)
        # itm_btn_7=self.set_btn('NEXT_STEP', step, quantity)
        # itm_btn_8=self.set_btn('APPLY', step, quantity)
        # itm_btn_9 = self.set_btn('<<', step, quantity)
        # self.markup.row(itm_btn_2, itm_btn_3, itm_btn_4)
        # self.markup.row(itm_btn_5, itm_btn_6, itm_btn_7)
        # self. markup.row(itm_btn_9, itm_btn_1, itm_btn_8)
        # return self.markup

    def set_inline_btn(self, name, text, step = 0, quantity = 0, message = None):
        if name == 'AMOUNT_ORDERS':
            config.KEYBOARD['AMOUNT_ORDERS'] = "{} {} {}".format(step + 1, ' из ', str(self.DB.count_rows_order(message.from_user.id)))
        if name == 'AMOUNT_PRODUCT':
            config.KEYBOARD['AMOUNT_PRODUCT'] = "{}".format(quantity)
        return InlineKeyboardButton(config.KEYBOARD[name], callback_data=text)

    #def set_select_category(self,category):
       # self.markup = InlineKeyboardMarkup(row_width=1)
        #for itm in self.DB.select_all_products_category(category):
            #self.markup.add(self.set_inline_btn(itm))
       #return self.markup
    def set_select_category(self,category, left,right, page, pages_count):
        self.markup = InlineKeyboardMarkup()
        left_btn = self.set_inline_btn('BACK_STEP', f'to_{left}_{category}')
        page_btn = InlineKeyboardButton(f"{str(page+1)}/{str(pages_count)}", callback_data='/')
        right_btn = self.set_inline_btn('NEXT_STEP', f'to_{right}_{category}')
        add_to_order_btn = self.set_inline_btn('ADD_TO_ORDER', f'add_{page}_{category}')
        self.markup.add(left_btn, page_btn, right_btn)
        self.markup.add(add_to_order_btn)
        return self.markup
    def pressed_btn_categoty_choose(self, category):
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1=self.set_btn('BACK_STEP')
        itm_btn_2=self.set_btn('NEXT_STEP')

