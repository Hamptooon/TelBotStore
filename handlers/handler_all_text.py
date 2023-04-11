from settings import config, utility
from handlers.handler import Handler
from settings.message import MESSAGES
import telebot
from telebot import types



class HandlerAllText(Handler):

    def __init__(self, bot):
        super().__init__(bot)
        self.step = 0

    def pressed_btn_product(self,message,product):
        self.bot.send_message(message.chat.id, 'Категория:  ' + config.KEYBOARD[product], reply_markup=self.keyboards.set_select_category(config.CATEGORY[product]))
        self.bot.send_message(message.chat.id,'Выберите товар...', reply_markup=self.keyboards.category_menu())
        # img = open(r'C:\Users\karac\Desktop\Scree.jpg', 'rb')
        # self.bot.send_photo(message.chat.id, img, caption="Овощь")

    def pressed_btn_category(self,message):
        self.bot.send_message(message.chat.id, 'Выберите категорию товара...', reply_markup=self.keyboards.category_menu())
    def pressed_btn_info(self, message):
        self.bot.send_message(message.chat.id, MESSAGES['trading_store'], parse_mode = "HTML", reply_markup=self.keyboards.info_menu())

    def pressed_btn_settings(self, message):
        self.bot.send_message(message.chat.id, MESSAGES['settings'], parse_mode = "HTML", reply_markup=self.keyboards.settings_menu())


    def pressed_btn_back(self, message):
        self.bot.send_message(message.chat.id, "Вы вернулись назад", reply_markup = self.keyboards.start_menu())
        print(message.chat.id)
    def pressed_btn_order(self, message):
        self.step = 0
        count = self.DB.select_all_products_id(message.from_user.id)
        quantity = self.DB.select_order_quantity(count[self.step], message.from_user.id)
        self.send_message_order(count[self.step], quantity, message)
    def send_message_order(self, product_id, quantity, message):
        self.bot.send_message(message.chat.id, MESSAGES['order_number'].format(self.step+1), parse_mode='HTML')
        self.bot.send_message(message.chat.id, MESSAGES['order'].format(self.DB.select_single_product_name(product_id),self.DB.select_single_product_price(product_id), self.DB.select_order_quantity(product_id, message.from_user.id)), parse_mode='HTML', reply_markup=self.keyboards.orders_menu(self.step, quantity, message))



    def pressed_btn_up(self, message):
        count = self.DB.select_all_products_id(message.from_user.id)
        quantity_order= self.DB.select_order_quantity(count[self.step], message.from_user.id)
        quantity_product=self.DB.select_single_product_quantity(count[self.step])
        if quantity_product>0:
            quantity_product-=1
            quantity_order+=1
            self.DB.update_product_value(count[self.step], 'quantity', quantity_product)
            self.DB.update_order_value(count[self.step], message.from_user.id,  'quantity', quantity_order)
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_down(self, message):
        count = self.DB.select_all_products_id(message.from_user.id)
        quantity_order = self.DB.select_order_quantity(count[self.step], message.from_user.id)
        quantity_product = self.DB.select_single_product_quantity(count[self.step])
        if quantity_order > 0 :
            quantity_order -= 1
            quantity_product+=1
            self.DB.update_order_value(count[self.step],message.from_user.id, 'quantity', quantity_order)
            self.DB.update_product_value(count[self.step], 'quantity', quantity_product)
        self.send_message_order(count[self.step], quantity_order, message)
    def  pressed_btn_x(self,message):
        count = self.DB.select_all_products_id(message.from_user.id)
        if count.__len__()>0:
            quantity_order = self.DB.select_order_quantity(count[self.step], message.from_user.id)

            quantity_product = self.DB.select_single_product_quantity(count[self.step])
            quantity_product+=quantity_order
            self.DB.delete_order(count[self.step], message.from_user.id)
            self.DB.update_product_value(count[self.step], 'quantity', quantity_product)
            self.step -= 1
            if self.step < 0:
                self.step = 0
        count = self.DB.select_all_products_id(message.from_user.id)
        if count.__len__()>0:

            quantity_order = self.DB.select_order_quantity(count[self.step], message.from_user.id)
            print(self.step)
            self.send_message_order(count[self.step], quantity_order, message)
        else:
            self.bot.send_message(message.chat.id, MESSAGES['no_orders'], parse_mode='HTML', reply_markup=self.keyboards.category_menu())
    def pressed_btn_back_step(self, message):
        if self.step > 0:
            self.step -= 1
        count = self.DB.select_all_products_id(message.from_user.id)
        quantity = self.DB.select_order_quantity(count[self.step], message.from_user.id)
        self.send_message_order(count[self.step], quantity, message)
    def pressed_btn_next_step(self, message):
        if self.step < self.DB.count_rows_order(message.from_user.id) - 1:
            self.step += 1
        count = self.DB.select_all_products_id(message.from_user.id)
        quantity = self.DB.select_order_quantity(count[self.step], message.from_user.id)
        self.send_message_order(count[self.step], quantity, message)

    def pressed_btn_apply(self, message):
        self.bot.send_message(message.chat.id, MESSAGES['apply'].format(utility.get_total_coast(self.DB), utility.get_total_quantity(self.DB)), parse_mode='HTML', reply_markup=self.keyboards.category_menu())
        self.DB.delete_all_order(message.from_user.id)

    def handle(self):

        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            if message.text == config.KEYBOARD['INFO']:
                self.pressed_btn_info(message)
            if message.text == config.KEYBOARD['SETTINGS']:
                self.pressed_btn_settings(message)
            if message.text == config.KEYBOARD['<<']:
                self.pressed_btn_back(message)
            if message.text == config.KEYBOARD['CHOOSE_GOODS']:
                self.pressed_btn_category(message)
            if message.text == config.KEYBOARD['ORDER']:
                if self.DB.count_rows_order(message.from_user.id)>0:
                    self.pressed_btn_order(message)
                else:
                    self.bot.send_message(message.chat.id, MESSAGES['no_orders'], parse_mode="HTML", reply_markup=self.keyboards.category_menu())




            if message.text == config.KEYBOARD['CLOTH']:
                self.pressed_btn_product(message, 'CLOTH')
            if message.text == config.KEYBOARD['FIGURINES']:
                self.pressed_btn_product(message,'FIGURINES')
            if message.text == config.KEYBOARD['MUGS']:
                self.pressed_btn_product(message,'MUGS')



            if message.text == config.KEYBOARD['UP']:
                self.pressed_btn_up(message)
            if message.text == config.KEYBOARD['DOWN']:
                self.pressed_btn_down(message)
            if message.text == config.KEYBOARD['X']:
                self.pressed_btn_x(message)
            if message.text == config.KEYBOARD['BACK_STEP']:
                self.pressed_btn_back_step(message)
            if message.text == config.KEYBOARD['NEXT_STEP']:
                self.pressed_btn_next_step(message)
            if message.text == config.KEYBOARD['APPLY']:
                self.pressed_btn_apply(message)
            # else:
            #     self.bot.send_message(message.chat.id, message.text)
