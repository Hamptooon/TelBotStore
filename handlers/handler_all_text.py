import os
import uuid

from settings import config, utility
from handlers.handler import Handler
from settings.message import MESSAGES
import telebot


class HandlerAllText(Handler):

    def __init__(self, bot):
        super().__init__(bot)
        self.step = 0
        self.step_admin = 0
        self.isPaginationChooseCall = False
        self.isPaginationProductsAdminCall = False
        self.isPaginationCartCall = False

    def pressed_btn_product_choose(self, message, category, i=0):
        pages_count = int(self.DB.select_count_products_in_category(category))
        all_products_id = self.DB.select_all_products_id_in_category(category)
        left = i - 1 if i != 0 else pages_count - 1
        right = i + 1 if i != pages_count - 1 else 0
        img_path = 'media/SHIZ.jpg'
        image_file = open(img_path, 'rb')
        image_data = image_file.read()
        image_file.close()
        name, price, quantity = self.DB.select_single_product_info(all_products_id[i])
        if not self.isPaginationChooseCall:
            self.isPaginationChooseCall = True
            self.bot.send_photo(message.chat.id, photo=image_data,
                                caption=f'{name}\nЦена: {price}\nКоличество на складе: {quantity}',
                                reply_markup=self.keyboards.set_select_category(message, category, left, right, i,
                                                                                pages_count))
        else:
            try:
                self.bot.edit_message_media(message_id=message.message_id, chat_id=message.chat.id,
                                        media=telebot.types.InputMedia(type='photo', media=image_data,
                                                                       caption=f'{name}\nЦена: {price}\nКоличество на '
                                                                               f'складе: {quantity}'),
                                        reply_markup=self.keyboards.set_select_category(message, category, left, right,
                                                                                        i, pages_count))
            except telebot.apihelper.ApiTelegramException:
                pass

    def pressed_btn_category_admin(self, message, category):
        self.step_admin = 0
        self.isPaginationProductsAdminCall = False
        count = self.DB.select_all_products_id_in_category(config.CATEGORY[category])
        self.send_message_product(count[self.step], message, category)

    def send_message_product(self, product_id, call, category):
        if type(call) == telebot.types.CallbackQuery:
            chat_id = call.message.chat.id
        elif type(call) == telebot.types.Message:
            chat_id = call.chat.id
        img_path = 'media/SHIZ.jpg'
        image_file = open(img_path, 'rb')
        image_data = image_file.read()
        image_file.close()
        name = self.DB.select_single_product_name(product_id)
        price = self.DB.select_single_product_price(product_id)
        quantity = self.DB.select_single_product_quantity(product_id)
        msg = f'{name}\nЦена: {price}\nКоличество на складе: {quantity}'
        if not self.isPaginationProductsAdminCall:
            self.isPaginationProductsAdminCall = True
            self.message = self.bot.send_photo(chat_id, photo=image_data,
                                               caption=msg, parse_mode="HTML",
                                               reply_markup=self.keyboards.change_menu(self.step_admin, quantity,
                                                                                       category, product_id))
        else:
            try:
                self.bot.edit_message_media(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                            media=telebot.types.InputMedia(type='photo', media=image_data,
                                                                           caption=msg, parse_mode="HTML"),
                                            reply_markup=self.keyboards.change_menu(self.step_admin, quantity, category,
                                                                                    product_id))
            except telebot.apihelper.ApiTelegramException:
                pass

    def pressed_btn_product(self, message, product_id):
        self.bot.send_message(message.chat.id, 'Категория:  ' + config.KEYBOARD[product_id])
        self.isPaginationChooseCall = False
        self.pressed_btn_product_choose(message=message, category=config.CATEGORY[product_id])
        self.bot.send_message(message.chat.id, 'Выберите товар...', reply_markup=self.keyboards.category_menu(message))

    def pressed_btn_category(self, message):
        self.bot.send_message(message.chat.id, 'Выберите категорию товара...',
                              reply_markup=self.keyboards.category_menu(message))

    def pressed_btn_info(self, message):
        self.bot.send_message(message.chat.id, MESSAGES['trading_store'], parse_mode="HTML",
                              reply_markup=self.keyboards.info_menu())

    def pressed_btn_settings(self, message):
        self.bot.send_message(message.chat.id, MESSAGES['settings'], parse_mode="HTML",
                              reply_markup=self.keyboards.settings_menu())

    def pressed_btn_back(self, message):
        self.bot.send_message(message.chat.id, "Вы вернулись в главное меню", reply_markup=self.keyboards.start_menu())

    def pressed_btn_back_admin(self, message):
        self.bot.send_message(message.chat.id, "Вы вернулись в главное меню",
                              reply_markup=self.keyboards.start_admin_menu())

    def pressed_btn_order(self, message):
        self.step = 0
        self.isPaginationCartCall = False
        count = self.DB.select_all_products_id(message.from_user.id)
        quantity = self.DB.select_order_quantity(count[self.step], message.from_user.id)
        self.send_message_order(count[self.step], quantity, message)
        self.bot.send_message(chat_id=message.from_user.id,
                              text='Можете отредактировать заказ или сразу перейти к оплате 😃',
                              reply_markup=self.keyboards.payment_menu())

    def send_message_order(self, product_id, quantity, call):
        if type(call) == telebot.types.CallbackQuery:
            chat_id = call.message.chat.id
        elif type(call) == telebot.types.Message:
            chat_id = call.chat.id
        msg = MESSAGES['order_info'].format(self.step + 1, self.DB.select_single_product_name(product_id),
                                            self.DB.select_single_product_price(product_id),
                                            self.DB.select_order_quantity(product_id, call.from_user.id))
        img_path = 'media/SHIZ.jpg'
        image_file = open(img_path, 'rb')
        image_data = image_file.read()
        image_file.close()
        if not self.isPaginationCartCall:
            self.isPaginationCartCall = True
            self.message = self.bot.send_photo(chat_id, photo=image_data,
                                               caption=msg, parse_mode="HTML",
                                               reply_markup=self.keyboards.orders_menu(self.step, quantity, call))
        else:
            try:
                self.bot.edit_message_media(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                            media=telebot.types.InputMedia(type='photo', media=image_data,
                                                                           caption=msg, parse_mode="HTML"),
                                            reply_markup=self.keyboards.orders_menu(self.step, quantity, call))
            except telebot.apihelper.ApiTelegramException:
                pass

    def pressed_btn_up(self, call):
        count = self.DB.select_all_products_id(call.from_user.id)
        quantity_order = self.DB.select_order_quantity(count[self.step], call.from_user.id)
        quantity_product = self.DB.select_single_product_quantity(count[self.step])
        if quantity_product > 0:
            quantity_product -= 1
            quantity_order += 1
            self.DB.update_product_value(count[self.step], 'quantity', quantity_product)
            self.DB.update_order_value(count[self.step], call.from_user.id, 'quantity', quantity_order)
        self.send_message_order(count[self.step], quantity_order, call)

    def pressed_btn_up_product_count(self, call, category):
        all_products_id_in_category = self.DB.select_all_products_id_in_category(config.CATEGORY[category])
        product_id = all_products_id_in_category[self.step_admin]
        quantity_product = self.DB.select_single_product_quantity(product_id)
        if quantity_product > 0:
            quantity_product += 1
            self.DB.update_product_value(product_id, 'quantity', quantity_product)
        self.send_message_product(product_id, call, category)

    def pressed_btn_down(self, call):
        count = self.DB.select_all_products_id(call.from_user.id)
        quantity_order = self.DB.select_order_quantity(count[self.step], call.from_user.id)
        quantity_product = self.DB.select_single_product_quantity(count[self.step])
        if quantity_order > 0:
            quantity_order -= 1
            quantity_product += 1
            self.DB.update_order_value(count[self.step], call.from_user.id, 'quantity', quantity_order)
            self.DB.update_product_value(count[self.step], 'quantity', quantity_product)
        self.send_message_order(count[self.step], quantity_order, call)

    def pressed_btn_down_product_count(self, call, category):
        all_products_id_in_category = self.DB.select_all_products_id_in_category(config.CATEGORY[category])
        product_id = all_products_id_in_category[self.step_admin]
        quantity_product = self.DB.select_single_product_quantity(product_id)
        if quantity_product > 0:
            quantity_product -= 1
            self.DB.update_product_value(product_id, 'quantity', quantity_product)
        self.send_message_product(product_id, call, category)

    def pressed_delete_btn(self, product_id, category, call):
        if self.DB.check_product_in_order(product_id):
            self.bot.answer_callback_query(call.id, MESSAGES['product_delete_prohibition'], show_alert=True)
        else:
            self.DB.delete_product(product_id)
            self.bot.answer_callback_query(call.id, MESSAGES['product_delete_successfully'], show_alert=True)
            self.step_admin = 0
            all_products_id_in_category = self.DB.select_all_products_id_in_category(config.CATEGORY[category])
            self.send_message_product(all_products_id_in_category[self.step_admin], call, category)

    def pressed_btn_change_photo(self, product_id, chat_id):
        # Запросите у пользователя новое фото товара
        self.bot.send_message(chat_id, "Пришлите новое фото товара:")

        # Получите новое фото товара от пользователя
        photo_message = self.bot.wait_for('photo')
        photo_file_id = photo_message.photo[-1].file_id
        photo_file = self.bot.get_file(photo_file_id)
        photo_data = self.bot.download_file(photo_file.file_path)

        # Сохраните новое фото товара в файловой системе
        filename = f"{uuid.uuid4()}.jpg"
        filepath = os.path.join("media", filename)
        with open(filepath, 'wb') as f:
            f.write(photo_data)

        # Обновите путь к фото товара в базе данных
        self.DB.update_product_photo(product_id, filepath)

        # Отправьте сообщение пользователю с подтверждением изменения фото товара
        self.bot.send_message(chat_id, "Фото товара успешно изменено!")
    def pressed_btn_x(self, call):
        count = self.DB.select_all_products_id(call.from_user.id)
        if count.__len__() > 0:
            quantity_order = self.DB.select_order_quantity(count[self.step], call.from_user.id)
            quantity_product = self.DB.select_single_product_quantity(count[self.step])
            quantity_product += quantity_order
            self.DB.delete_order(count[self.step], call.from_user.id)
            self.DB.update_product_value(count[self.step], 'quantity', quantity_product)
            self.step -= 1
            if self.step < 0:
                self.step = 0
        count = self.DB.select_all_products_id(call.from_user.id)
        if count.__len__() > 0:
            quantity_order = self.DB.select_order_quantity(count[self.step], call.from_user.id)
            self.send_message_order(count[self.step], quantity_order, call)
        else:
            self.bot.send_message(call.message.chat.id, MESSAGES['no_orders'], parse_mode='HTML',
                                  reply_markup=self.keyboards.category_menu())

    def pressed_btn_back_step(self, call):
        if self.step > 0:
            self.step -= 1
        elif self.step == 0:
            self.step = self.DB.count_rows_order(call.from_user.id) - 1
        count = self.DB.select_all_products_id(call.from_user.id)
        quantity = self.DB.select_order_quantity(count[self.step], call.from_user.id)
        self.send_message_order(count[self.step], quantity, call)

    def pressed_btn_back_step_admin(self, call, category):
        if self.step_admin > 0:
            self.step_admin -= 1
        elif self.step_admin == 0:
            self.step_admin = self.DB.count_rows_products_in_category(config.CATEGORY[category]) - 1
        all_products_id_in_category = self.DB.select_all_products_id_in_category(config.CATEGORY[category])
        self.send_message_product(all_products_id_in_category[self.step_admin], call, category)

    def pressed_btn_next_step(self, call):
        if self.step < self.DB.count_rows_order(call.from_user.id) - 1:
            self.step += 1
        else:
            self.step = 0
        count = self.DB.select_all_products_id(call.from_user.id)
        quantity = self.DB.select_order_quantity(count[self.step], call.from_user.id)
        self.send_message_order(count[self.step], quantity, call)

    def pressed_btn_next_step_admin(self, call, category):
        if self.step_admin < self.DB.count_rows_products_in_category(config.CATEGORY[category]) - 1:
            self.step_admin += 1
        else:
            self.step_admin = 0
        all_products_id_in_category = self.DB.select_all_products_id_in_category(config.CATEGORY[category])
        self.send_message_product(all_products_id_in_category[self.step_admin], call, category)

    def pressed_btn_apply(self, message):
        self.bot.send_message(message.chat.id, MESSAGES['apply'].format(utility.get_total_coast(self.DB, message),
                                                                        utility.get_total_quantity(self.DB, message)),
                              parse_mode='HTML', reply_markup=self.keyboards.category_menu(message))
        self.DB.add_user_info(message.from_user.id, message.from_user.first_name, message.from_user.last_name,
                              '@' + message.from_user.username)
        client = self.DB.select_user(message.from_user.id)
        self.bot.send_message(config.ADMIN_ID, text=str(client), parse_mode="HTML")

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
                if self.DB.count_rows_order(message.from_user.id) > 0:
                    self.pressed_btn_order(message)
                else:
                    self.bot.send_message(message.chat.id, MESSAGES['no_orders'], parse_mode="HTML",
                                          reply_markup=self.keyboards.category_menu())
            if message.text == config.KEYBOARD['CHANGE_PRODUCTS']:
                self.pressed_btn_category(message)
            if message.text == config.KEYBOARD['MAIN_MENU']:
                self.pressed_btn_back_admin(message)

            if message.text == config.KEYBOARD['CLOTH']:
                if message.from_user.id == config.ADMIN_ID:
                    self.pressed_btn_category_admin(message, 'CLOTH')
                else:
                    self.pressed_btn_product(message, 'CLOTH')
            if message.text == config.KEYBOARD['FIGURINES']:
                if message.from_user.id == config.ADMIN_ID:
                    self.pressed_btn_category_admin(message, 'FIGURINES')
                else:
                    self.pressed_btn_product(message, 'FIGURINES')
            if message.text == config.KEYBOARD['MUGS']:
                if message.from_user.id == config.ADMIN_ID:
                    self.pressed_btn_category_admin(message, 'MUGS')
                else:
                    self.pressed_btn_product(message, 'MUGS')
            if message.text == config.KEYBOARD['APPLY']:
                print(message.from_user.id)
                self.pressed_btn_apply(message)

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            is_order_present = self.DB.check_order_present(call.from_user.id)
            if 'to' in call.data:
                page = int(call.data.split('_')[1])
                category = call.data.split('_')[2]
                self.pressed_btn_product_choose(call.message, category, i=page)
            elif 'add' in call.data:
                page = int(call.data.split('_')[1])
                category = call.data.split('_')[2]
                all_products_id = self.DB.select_all_products_id_in_category(category)
                product_id = all_products_id[page]
                self.DB.add_order(1, product_id, call.from_user.id)
                self.bot.answer_callback_query(call.id,
                                               MESSAGES['product_order'].format(
                                                   self.DB.select_single_product_name(product_id),
                                                   self.DB.select_single_product_price(product_id),
                                                   self.DB.select_single_product_quantity(product_id)), show_alert=True)
                self.pressed_btn_product_choose(message=call.message, category=category, i=page)
            elif call.data == 'down_count' and is_order_present:
                self.pressed_btn_down(call)
            elif call.data == 'up_count' and is_order_present:
                self.pressed_btn_up(call)
            elif call.data == 'back_product' and is_order_present:
                self.pressed_btn_back_step(call)
            elif call.data == 'next_product' and is_order_present:
                self.pressed_btn_next_step(call)
            elif call.data == 'delete_product_from_order' and is_order_present:
                self.pressed_btn_x(call)
            elif 'up_product_count' in call.data:
                self.pressed_btn_up_product_count(call, call.data.split('_')[3])
            elif 'down_product_count' in call.data:
                self.pressed_btn_down_product_count(call, call.data.split('_')[3])
            elif 'next_product' in call.data:
                self.pressed_btn_next_step_admin(call, call.data.split('_')[2])
            elif 'back_product' in call.data:
                self.pressed_btn_back_step_admin(call, call.data.split('_')[2])
            elif 'delete_product' in call.data:
                self.pressed_delete_btn(call.data.split('_')[2], call.data.split('_')[3], call)
            elif 'change_image' in call.data:
                self.pressed_btn_change_photo(call.data.split('_')[2], call.message.chat.id)
