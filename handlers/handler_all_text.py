from settings import config, utility
from handlers.handler import Handler
# from handlers.handler_inline_query import HandlerInlineQuery

from settings.message import MESSAGES
import telebot
from telebot import types


class HandlerAllText(Handler):

    def __init__(self, bot):
        super().__init__(bot)
        self.step = 0
        self.isPaginationChooseCall = False
        self.isPaginationCartCall = False
    def pressed_btn_product_choose(self, message, category, i = 0):
        pages_count = int(self.DB.select_count_products_in_category(category))
        all_products_id = self.DB.select_all_products_id_in_category(category)
        left = i - 1 if i != 0 else pages_count - 1
        right = i + 1 if i != pages_count - 1 else 0
        img_path = 'media/SHIZ.jpg'
        image_file = open(img_path, 'rb')
        image_data = image_file.read()
        image_file.close()
        name = self.DB.select_single_product_name(all_products_id[i])
        price = self.DB.select_single_product_price(all_products_id[i])
        quantity = self.DB.select_single_product_quantity(all_products_id[i])
        if self.isPaginationChooseCall == False:
            self.isPaginationChooseCall = True
            self.bot.send_photo(message.chat.id, photo=image_data,
                                        caption=f'{name}\nЦена: {price}\nКоличество на складе: {quantity}', reply_markup=self.keyboards.set_select_category(category, left, right, i, pages_count))

        else:
            self.bot.edit_message_media(message_id= message.message_id,chat_id = message.chat.id, media=telebot.types.InputMedia(type='photo', media=image_data,caption=f'{name}\nЦена: {price}\nКоличество на складе: {quantity}'), reply_markup=self.keyboards.set_select_category(category, left, right, i, pages_count))
    def pressed_btn_product(self,message,product_id):
        self.bot.send_message(message.chat.id, 'Категория:  ' + config.KEYBOARD[product_id])
        self.isPaginationChooseCall = False
        self.pressed_btn_product_choose(message=message, category=config.CATEGORY[product_id])
        self.bot.send_message(message.chat.id,'Выберите товар...', reply_markup=self.keyboards.category_menu())
    def pressed_btn_category(self,message):
        self.bot.send_message(message.chat.id, 'Выберите категорию товара...', reply_markup=self.keyboards.category_menu())
    def pressed_btn_info(self, message):
        self.bot.send_message(message.chat.id, MESSAGES['trading_store'], parse_mode = "HTML", reply_markup=self.keyboards.info_menu())

    def pressed_btn_settings(self, message):
        self.bot.send_message(message.chat.id, MESSAGES['settings'], parse_mode = "HTML", reply_markup=self.keyboards.settings_menu())


    def pressed_btn_back(self, message):
        self.bot.send_message(message.chat.id, "Вы вернулись в главное меню", reply_markup = self.keyboards.start_menu())
        print(message.chat.id)
    def pressed_btn_order(self, message):
        self.step = 0
        self.isPaginationCartCall = False
        count = self.DB.select_all_products_id(message.from_user.id)
        quantity = self.DB.select_order_quantity(count[self.step], message.from_user.id)
        self.send_message_order(count[self.step], quantity, message)
        self.bot.send_message(chat_id= message.from_user.id, text = 'Можете отредактировать заказ или сразу перейти к оплате 😃', reply_markup=self.keyboards.payment_menu())
    def send_message_order(self, product_id, quantity, call):
        print(type(call))
        if type(call) == telebot.types.CallbackQuery:
            print('-----')
            chat_id = call.message.chat.id
        elif type(call) == telebot.types.Message:
            print('++++++')
            chat_id = call.chat.id
        msg = MESSAGES['order_info'].format(self.step + 1, self.DB.select_single_product_name(product_id),
                                       self.DB.select_single_product_price(product_id),
                                       self.DB.select_order_quantity(product_id, call.from_user.id))
        img_path = 'media/SHIZ.jpg'
        image_file = open(img_path, 'rb')
        image_data = image_file.read()
        image_file.close()
        if self.isPaginationCartCall == False:
            self.isPaginationCartCall = True
            self.message = self.bot.send_photo(chat_id, photo=image_data,
                                               caption=msg,parse_mode="HTML",
                                               reply_markup=self.keyboards.orders_menu(self.step, quantity, call))
        else:
            try:
                self.bot.edit_message_media(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                            media=telebot.types.InputMedia(type='photo', media=image_data,
                                                                           caption=msg,parse_mode="HTML"), reply_markup=self.keyboards.orders_menu(self.step, quantity, call))
            except: pass
        # self.bot.send_message(message.chat.id, MESSAGES['order_number'].format(self.step+1), parse_mode='HTML')
        # self.bot.send_message(message.chat.id, MESSAGES['order'].format(self.DB.select_single_product_name(product_id),self.DB.select_single_product_price(product_id), self.DB.select_order_quantity(product_id, message.from_user.id)), parse_mode='HTML', reply_markup=self.keyboards.orders_menu(self.step, quantity, message))



    def pressed_btn_up(self, call):
        count = self.DB.select_all_products_id(call.from_user.id)
        quantity_order= self.DB.select_order_quantity(count[self.step], call.from_user.id)
        quantity_product=self.DB.select_single_product_quantity(count[self.step])
        if quantity_product>0:
            quantity_product-=1
            quantity_order+=1
            self.DB.update_product_value(count[self.step], 'quantity', quantity_product)
            self.DB.update_order_value(count[self.step], call.from_user.id,  'quantity', quantity_order)
        self.send_message_order(count[self.step], quantity_order, call)

    def pressed_btn_down(self, call):
        count = self.DB.select_all_products_id(call.from_user.id)
        quantity_order = self.DB.select_order_quantity(count[self.step], call.from_user.id)
        quantity_product = self.DB.select_single_product_quantity(count[self.step])
        if quantity_order > 0 :
            quantity_order -= 1
            quantity_product+=1
            self.DB.update_order_value(count[self.step],call.from_user.id, 'quantity', quantity_order)
            self.DB.update_product_value(count[self.step], 'quantity', quantity_product)
        self.send_message_order(count[self.step], quantity_order, call)
    def  pressed_btn_x(self,call):
        count = self.DB.select_all_products_id(call.from_user.id)
        if count.__len__()>0:
            quantity_order = self.DB.select_order_quantity(count[self.step], call.from_user.id)

            quantity_product = self.DB.select_single_product_quantity(count[self.step])
            quantity_product+=quantity_order
            self.DB.delete_order(count[self.step], call.from_user.id)
            self.DB.update_product_value(count[self.step], 'quantity', quantity_product)
            self.step -= 1
            if self.step < 0:
                self.step = 0
        count = self.DB.select_all_products_id(call.from_user.id)
        if count.__len__()>0:

            quantity_order = self.DB.select_order_quantity(count[self.step], call.from_user.id)
            print(self.step)
            self.send_message_order(count[self.step], quantity_order, call)
        else:
            self.bot.send_message(call.message.chat.id, MESSAGES['no_orders'], parse_mode='HTML', reply_markup=self.keyboards.category_menu())
    def pressed_btn_back_step(self, call):
        if self.step > 0:
            self.step -= 1
        elif self.step == 0:
            self.step = self.DB.count_rows_order(call.from_user.id) - 1
        count = self.DB.select_all_products_id(call.from_user.id)
        quantity = self.DB.select_order_quantity(count[self.step], call.from_user.id)
        self.send_message_order(count[self.step], quantity, call)
    def pressed_btn_next_step(self, call):
        print(self.step)
        print(self.DB.count_rows_order(call.from_user.id))
        if self.step < self.DB.count_rows_order(call.from_user.id) - 1:
            self.step += 1
        else: self.step = 0

        print(call.from_user.id)
        count = self.DB.select_all_products_id(call.from_user.id)
        print(len(count))
        quantity = self.DB.select_order_quantity(count[self.step], call.from_user.id)
        self.send_message_order(count[self.step], quantity, call)

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



            # if message.text == config.KEYBOARD['UP']:
            #     self.pressed_btn_up(message)
            # if message.text == config.KEYBOARD['DOWN']:
            #     self.pressed_btn_down(message)
            # if message.text == config.KEYBOARD['X']:
            #     self.pressed_btn_x(message)
            # if message.text == config.KEYBOARD['BACK_STEP']:
            #     self.pressed_btn_back_step(message)
            # if message.text == config.KEYBOARD['NEXT_STEP']:
            #     self.pressed_btn_next_step(message)
            if message.text == config.KEYBOARD['APPLY']:
                self.pressed_btn_apply(message)
            # else:
            #     self.bot.send_message(message.chat.id, message.text)

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            isOrderPresent = self.DB.check_order_present(call.from_user.id)
            if 'to' in call.data:
                page = int(call.data.split('_')[1])
                category = call.data.split('_')[2]
                self.pressed_btn_product_choose(call.message, category, i=page)
            elif 'add' in call.data:
                page = int(call.data.split('_')[1])
                category = call.data.split('_')[2]
                all_products_id = self.DB.select_all_products_id_in_category(category)
                product_id = all_products_id[page]
                self.DB._add_orders(1, product_id, call.from_user.id)
                self.bot.answer_callback_query(call.id,
                                               MESSAGES['product_order'].format(self.DB.select_single_product_name(product_id ),
                                                                                self.DB.select_single_product_price(product_id ),
                                                                                self.DB.select_single_product_quantity(product_id )),
                                               show_alert=True)
                self.pressed_btn_product_choose(message=call.message, category=category, i=page)
            elif call.data == 'down_count' and isOrderPresent:
                self.pressed_btn_down(call)
            elif call.data == 'up_count' and isOrderPresent:
                self.pressed_btn_up(call)
            elif call.data == 'back_product' and isOrderPresent:
                self.pressed_btn_back_step(call)
            elif call.data == 'next_product' and isOrderPresent:
                self.pressed_btn_next_step(call)
            elif call.data == 'delete_product' and isOrderPresent:
                self.pressed_btn_x(call)

                # down_btn = self.set_inline_btn('DOWN', 'down_count')
                # amount_product_btn = self.set_inline_btn('AMOUNT_PRODUCT', 'amount_product', quantity=quantity)
                # up_btn = self.set_inline_btn('UP', 'up_product')
                # back_step_btn = self.set_inline_btn('BACK_STEP', 'back_product')
                # amount_orders_btn = self.set_inline_btn('AMOUNT_ORDERS', 'amount_orders', step=step, message=message)
                # next_step_btn = self.set_inline_btn('NEXT_STEP', 'next_product')
                # delete_btn = self.set_inline_btn('X', 'delete_product')
