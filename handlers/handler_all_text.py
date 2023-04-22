from aiogram.dispatcher import FSMContext

from settings import config, utility
from handlers.handler import Handler
from settings.message import MESSAGES
from aiogram import types, utils
import io
from PIL import Image

from states.states import ProductChangeStatesGroup


class HandlerAllText(Handler):

    def __init__(self, bot, dp):
        super().__init__(bot, dp)
        self.step = 0
        self.step_admin = 0
        self.isPaginationChooseCall = False
        self.isPaginationProductsAdminCall = False
        self.isPaginationCartCall = False

    async def send_info_product(self, message, category_id, i=0):
        pages_count = int(self.DB.select_count_products_in_category(category_id))
        all_products_id = self.DB.select_all_products_id_in_category(category_id)
        left = i - 1 if i != 0 else pages_count - 1
        right = i + 1 if i != pages_count - 1 else 0
        img_path = self.DB.select_single_product_image_path(all_products_id[i])
        name, price, quantity = self.DB.select_single_product_info(all_products_id[i])
        with open(img_path, "rb") as file:
            image = Image.open(file)
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="JPEG")
            image_bytes.seek(0)
        product_info_message = f'{name}\nЦена: {price}\nКоличество на складе: {quantity}'
        if not self.isPaginationChooseCall:
            self.isPaginationChooseCall = True
            await self.bot.send_photo(chat_id=message.chat.id, photo=image_bytes,
                                      caption=product_info_message,
                                      reply_markup=self.keyboards.set_select_category(category_id, left, right,
                                                                                      i,
                                                                                      pages_count))
        else:
            try:
                await self.bot.edit_message_media(message_id=message.message_id, chat_id=message.chat.id,
                                                  media=types.InputMediaPhoto(type='photo', media=image_bytes,
                                                                              caption=product_info_message),
                                                  reply_markup=self.keyboards.set_select_category(category_id,
                                                                                                  left, right,
                                                                                                  i, pages_count))
            except utils.exceptions.MessageNotModified:
                pass

    async def pressed_btn_category_admin(self, message, category):
        self.step_admin = 0
        self.isPaginationProductsAdminCall = False
        all_products_id_in_category = self.DB.select_all_products_id_in_category(config.CATEGORY[category])
        await self.send_info_product_admin(all_products_id_in_category[self.step], message, category)

    async def send_info_product_admin(self, product_id, call, category):
        if type(call) == types.CallbackQuery:
            chat_id = call.message.chat.id
        else:
            chat_id = call.chat.id
        img_path = self.DB.select_single_product_image_path(product_id)
        with open(img_path, "rb") as file:
            image = Image.open(file)
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="JPEG")
            image_bytes.seek(0)
        name, price, quantity = self.DB.select_single_product_info(product_id)
        msg = f'{name}\nЦена: {price}\nКоличество на складе: {quantity}'
        if not self.isPaginationProductsAdminCall:
            self.isPaginationProductsAdminCall = True
            await self.bot.send_photo(chat_id=chat_id, photo=image_bytes,
                                      caption=msg, parse_mode="HTML",
                                      reply_markup=self.keyboards.change_menu_admin(self.step_admin, quantity,
                                                                                    category, product_id))
        else:
            try:
                await self.bot.edit_message_media(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                                  media=types.InputMedia(type='photo', media=image_bytes,
                                                                         caption=msg, parse_mode="HTML"),
                                                  reply_markup=self.keyboards.change_menu_admin(self.step_admin,
                                                                                                quantity,
                                                                                                category,
                                                                                                product_id))
            except utils.exceptions.MessageNotModified:
                pass

    async def pressed_btn_category(self, message, product_id):
        await self.bot.send_message(chat_id=message.chat.id, text='Категория:  ' + config.KEYBOARD[product_id])
        self.isPaginationChooseCall = False
        await self.send_info_product(message=message, category_id=config.CATEGORY[product_id])
        await self.bot.send_message(chat_id=message.chat.id, text='Выберите товар...',
                                    reply_markup=self.keyboards.category_menu(message))

    async def pressed_btn_choose_category(self, message):
        await self.bot.send_message(chat_id=message.chat.id, text='Выберите категорию товара...',
                                    reply_markup=self.keyboards.category_menu(message))

    async def pressed_btn_info(self, message):
        await self.bot.send_message(chat_id=message.chat.id, text=MESSAGES['trading_store'], parse_mode="HTML",
                                    reply_markup=self.keyboards.info_menu())

    async def pressed_btn_settings(self, message):
        await self.bot.send_message(chat_id=message.chat.id, text=MESSAGES['settings'], parse_mode="HTML",
                                    reply_markup=self.keyboards.settings_menu())

    async def pressed_btn_back(self, message):
        await self.bot.send_message(chat_id=message.chat.id, text="Вы вернулись в главное меню",
                                    reply_markup=self.keyboards.start_menu())

    async def pressed_btn_back_admin(self, message):
        await self.bot.send_message(chat_id=message.chat.id, text="Вы вернулись в главное меню",
                                    reply_markup=self.keyboards.start_admin_menu())

    async def pressed_btn_shopping_cart(self, message):
        self.step = 0
        self.isPaginationCartCall = False
        all_products_id_in_order_by_user = self.DB.select_all_products_id_in_order_by_user(message.from_user.id)
        await self.send_info_products_in_order(all_products_id_in_order_by_user[self.step],
                                               message)
        await self.bot.send_message(chat_id=message.from_user.id,
                                    text='Можете отредактировать заказ или сразу перейти к оплате 😃',
                                    reply_markup=self.keyboards.payment_menu())

    async def send_info_products_in_order(self, product_id, call):
        if type(call) == types.CallbackQuery:
            chat_id = call.message.chat.id
        else:
            chat_id = call.chat.id
        name, price, quantity = self.DB.select_single_product_info_in_shopping_cart(product_id, call.from_user.id)
        msg = MESSAGES['order_info'].format(self.step + 1, name, price, quantity, call.from_user.id)
        img_path = self.DB.select_single_product_image_path(product_id)

        with open(img_path, "rb") as file:
            image = Image.open(file)
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="JPEG")
            image_bytes.seek(0)
        if not self.isPaginationCartCall:
            self.isPaginationCartCall = True
            await self.bot.send_photo(chat_id=chat_id, photo=image_bytes,
                                      caption=msg, parse_mode="HTML",
                                      reply_markup=self.keyboards.orders_menu(self.step, quantity, call))
        else:
            try:
                await self.bot.edit_message_media(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                                  media=types.InputMedia(type='photo', media=image_bytes,
                                                                         caption=msg, parse_mode="HTML"),
                                                  reply_markup=self.keyboards.orders_menu(self.step, quantity, call))
            except utils.exceptions.MessageNotModified:
                pass

    async def pressed_btn_up(self, call):
        count = self.DB.select_all_products_id_in_order_by_user(call.from_user.id)
        quantity_order = self.DB.select_quantity_product_in_order(count[self.step], call.from_user.id)
        quantity_product = self.DB.select_single_product_quantity(count[self.step])
        if quantity_product > 0:
            quantity_product -= 1
            quantity_order += 1
            self.DB.update_product_value(count[self.step], 'quantity', quantity_product)
            self.DB.update_order_value(count[self.step], call.from_user.id, 'quantity', quantity_order)
        await self.send_info_products_in_order(count[self.step], call)

    async def pressed_btn_up_admin(self, call, category):
        all_products_id_in_category = self.DB.select_all_products_id_in_category(config.CATEGORY[category])
        product_id = all_products_id_in_category[self.step_admin]
        quantity_product = self.DB.select_single_product_quantity(product_id)
        if quantity_product > 0:
            quantity_product += 1
            self.DB.update_product_value(product_id, 'quantity', quantity_product)
        await self.send_info_product_admin(product_id, call, category)

    async def pressed_btn_down(self, call):
        count = self.DB.select_all_products_id_in_order_by_user(call.from_user.id)
        quantity_order = self.DB.select_quantity_product_in_order(count[self.step], call.from_user.id)
        quantity_product = self.DB.select_single_product_quantity(count[self.step])
        if quantity_order > 1:
            quantity_order -= 1
            quantity_product += 1
            self.DB.update_order_value(count[self.step], call.from_user.id, 'quantity', quantity_order)
            self.DB.update_product_value(count[self.step], 'quantity', quantity_product)
        await self.send_info_products_in_order(count[self.step], call)

    async def pressed_btn_down_admin(self, call, category):
        all_products_id_in_category = self.DB.select_all_products_id_in_category(config.CATEGORY[category])
        product_id = all_products_id_in_category[self.step_admin]
        quantity_product = self.DB.select_single_product_quantity(product_id)
        if quantity_product > 0:
            quantity_product -= 1
            self.DB.update_product_value(product_id, 'quantity', quantity_product)
        await self.send_info_product_admin(product_id, call, category)

    async def pressed_btn_delete_product_admin(self, product_id, category, call):
        if self.DB.check_product_in_order(product_id):
            self.bot.answer_callback_query(call.id, MESSAGES['product_delete_prohibition'], show_alert=True)
        else:
            self.DB.delete_product(product_id)
            self.bot.answer_callback_query(call.id, MESSAGES['product_delete_successfully'], show_alert=True)
            self.step_admin = 0
            all_products_id_in_category = self.DB.select_all_products_id_in_category(config.CATEGORY[category])
            await self.send_info_product_admin(all_products_id_in_category[self.step_admin], call, category)

    async def pressed_btn_delete_product(self, call):
        all_products_id = self.DB.select_all_products_id_in_order_by_user(call.from_user.id)
        if all_products_id.__len__() > 0:
            quantity_order = self.DB.select_quantity_product_in_order(all_products_id[self.step], call.from_user.id)
            quantity_product = self.DB.select_single_product_quantity(all_products_id[self.step])
            quantity_product += quantity_order
            self.DB.delete_order(all_products_id[self.step], call.from_user.id)
            self.DB.update_product_value(all_products_id[self.step], 'quantity', quantity_product)
            self.step -= 1
            if self.step < 0:
                self.step = 0
        all_products_id = self.DB.select_all_products_id_in_order_by_user(call.from_user.id)
        if all_products_id.__len__() > 0:
            await self.send_info_products_in_order(all_products_id[self.step], call)
        else:
            print(99999)
            await self.bot.send_message(call.message.chat.id, MESSAGES['no_orders'], parse_mode='HTML',
                                        reply_markup=self.keyboards.category_menu(call.message))

    async def pressed_btn_previous_product(self, call):
        if self.step > 0:
            self.step -= 1
        elif self.step == 0:
            self.step = self.DB.count_rows_order(call.from_user.id) - 1
        count = self.DB.select_all_products_id_in_order_by_user(call.from_user.id)
        await self.send_info_products_in_order(count[self.step], call)

    async def pressed_btn_previous_product_admin(self, call, category):
        if self.step_admin > 0:
            self.step_admin -= 1
        elif self.step_admin == 0:
            self.step_admin = self.DB.count_rows_products_in_category(config.CATEGORY[category]) - 1
        all_products_id_in_category = self.DB.select_all_products_id_in_category(config.CATEGORY[category])
        await self.send_info_product_admin(all_products_id_in_category[self.step_admin], call, category)

    async def pressed_btn_next_step(self, call):
        if self.step < self.DB.count_rows_order(call.from_user.id) - 1:
            self.step += 1
        else:
            self.step = 0
        count = self.DB.select_all_products_id_in_order_by_user(call.from_user.id)
        await self.send_info_products_in_order(count[self.step], call)

    async def pressed_btn_next_step_admin(self, call, category):
        if self.step_admin < self.DB.count_rows_products_in_category(config.CATEGORY[category]) - 1:
            self.step_admin += 1
        else:
            self.step_admin = 0
        all_products_id_in_category = self.DB.select_all_products_id_in_category(config.CATEGORY[category])
        await self.send_info_product_admin(all_products_id_in_category[self.step_admin], call, category)

    async def pressed_btn_apply(self, message):
        total_cost = utility.get_total_coast(self.DB, message)
        total_quantity = utility.get_total_quantity(self.DB, message)
        apply_message = MESSAGES['apply'].format(total_cost, total_quantity)
        await self.bot.send_message(message.chat.id, apply_message, parse_mode='HTML',
                                    reply_markup=self.keyboards.category_menu(message))
        self.DB.add_user_info(message.from_user.id, message.from_user.first_name, message.from_user.last_name,
                              '@' + message.from_user.username)
        client = self.DB.select_user(message.from_user.id)
        await self.bot.send_message(config.ADMIN_ID, text=str(client), parse_mode="HTML")

    async def pressed_btn_change_name_product_admin(self, product_id, chat_id):
        await self.bot.send_message(chat_id=chat_id, text='Введите новое название товара...')
        await ProductChangeStatesGroup.name.set()

    async def handle(self):
        @self.dp.message_handler(content_types=types.ContentTypes.ANY)
        async def handle(message: types.Message):
            if message.text == config.KEYBOARD['INFO']:
                await self.pressed_btn_info(message)
            elif message.text == config.KEYBOARD['SETTINGS']:
                await self.pressed_btn_settings(message)
            elif message.text == config.KEYBOARD['<<']:
                await self.pressed_btn_back(message)
            elif message.text == config.KEYBOARD['CHOOSE_GOODS']:
                await self.pressed_btn_choose_category(message)
            elif message.text == config.KEYBOARD['ORDER']:
                if self.DB.count_rows_order(message.from_user.id) > 0:
                    await self.pressed_btn_shopping_cart(message)
                else:
                    await self.bot.send_message(chat_id=message.chat.id, text=MESSAGES['no_orders'], parse_mode="HTML",
                                                reply_markup=self.keyboards.category_menu(message))
            elif message.text == config.KEYBOARD['CHANGE_PRODUCTS']:
                await self.pressed_btn_choose_category(message)
            elif message.text == config.KEYBOARD['MAIN_MENU']:
                await self.pressed_btn_back_admin(message)

            elif message.text == config.KEYBOARD['CLOTH']:
                if message.from_user.id == config.ADMIN_ID:
                    await self.pressed_btn_category_admin(message, 'CLOTH')
                else:
                    await self.pressed_btn_category(message, 'CLOTH')
            elif message.text == config.KEYBOARD['FIGURINES']:
                if message.from_user.id == config.ADMIN_ID:
                    await self.pressed_btn_category_admin(message, 'FIGURINES')
                else:
                    await self.pressed_btn_category(message, 'FIGURINES')
            elif message.text == config.KEYBOARD['MUGS']:
                if message.from_user.id == config.ADMIN_ID:
                    await self.pressed_btn_category_admin(message, 'MUGS')
                else:
                    await self.pressed_btn_category(message, 'MUGS')
            elif message.text == config.KEYBOARD['APPLY']:
                await self.pressed_btn_apply(message)

        #
        @self.dp.callback_query_handler(lambda call: not call.data.startswith('change'))
        async def callback_inline(call: types.CallbackQuery):
            is_order_present = self.DB.check_order_present(call.from_user.id)
            if 'to' in call.data:
                page = int(call.data.split('_')[1])
                category_id = call.data.split('_')[2]
                await self.send_info_product(call.message, category_id, i=page)
            elif 'add' in call.data:
                page = int(call.data.split('_')[1])
                category_id = call.data.split('_')[2]
                all_products_id = self.DB.select_all_products_id_in_category(category_id)
                product_id = all_products_id[page]
                self.DB.add_order(1, product_id, call.from_user.id)
                name, price, quantity = self.DB.select_single_product_info(product_id)
                add_product_message = MESSAGES['product_order'].format(name, price, quantity)
                await self.bot.answer_callback_query(call.id, add_product_message, show_alert=True)
                await self.send_info_product(message=call.message, category_id=category_id, i=page)
            elif call.data == 'down_count':
                if is_order_present:
                    await self.pressed_btn_down(call)
                else:
                    await self.bot.answer_callback_query(call.id, MESSAGES['no_orders'], show_alert=True)
            elif call.data == 'up_count':
                if is_order_present:
                    await self.pressed_btn_up(call)
                else:
                    await self.bot.answer_callback_query(call.id, MESSAGES['no_orders'], show_alert=True)
            elif call.data == 'back_product':
                if is_order_present:
                    await self.pressed_btn_previous_product(call)
                else:
                    await self.bot.answer_callback_query(call.id, MESSAGES['no_orders'], show_alert=True)
            elif call.data == 'next_product':
                if is_order_present:
                    await self.pressed_btn_next_step(call)
                else:
                    await self.bot.answer_callback_query(call.id, MESSAGES['no_orders'], show_alert=True)
            elif call.data == 'delete_product_from_order':
                if is_order_present:
                    await self.pressed_btn_delete_product(call)
                else:
                    await self.bot.answer_callback_query(call.id, MESSAGES['no_orders'], show_alert=True)
            elif 'up_product_count' in call.data:
                await self.pressed_btn_up_admin(call, call.data.split('_')[3])
            elif 'down_product_count' in call.data:
                await self.pressed_btn_down_admin(call, call.data.split('_')[3])
            elif 'next_product' in call.data:
                await self.pressed_btn_next_step_admin(call, call.data.split('_')[2])
            elif 'back_product' in call.data:
                await self.pressed_btn_previous_product_admin(call, call.data.split('_')[2])
            elif 'delete_product' in call.data:
                await self.pressed_btn_delete_product_admin(call.data.split('_')[2], call.data.split('_')[3], call)
            # elif 'change_image' in call.data:
            #     await self.pressed_btn_change_product_photo_admin(call.data.split('_')[2], call.message.chat.id)
            # elif 'change_name' in call.data:
            #     await self.pressed_btn_change_name_product_admin(call.data.split('_')[2], call.message.chat.id)

        @self.dp.callback_query_handler(lambda call: call.data and call.data.startswith('change'))
        async def pressed_btn_change_name_product(call: types.CallbackQuery, state: FSMContext):
            # Получаем идентификатор товара из callback data
            print('change_name')
            product_id = int(call.data.split('_')[2])

            # Запоминаем идентификатор товара в состоянии
            async with state.proxy() as data:
                data['product_id'] = product_id

            # Отправляем сообщение с просьбой ввести новое имя товара
            await self.bot.send_message(chat_id=call.message.chat.id, text='Введите новое значение...')

            # Переводим пользователя в состояние, в котором он может ввести новое имя товара
            if 'change_name' in call.data:
                await ProductChangeStatesGroup.name.set()
            elif 'change_price' in call.data:
                await ProductChangeStatesGroup.price.set()
            elif 'change_image' in call.data:
                print('change_image')
                await ProductChangeStatesGroup.image.set()

        @self.dp.message_handler(state=ProductChangeStatesGroup.name)
        async def change_name(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                product_id = data['product_id']
            self.DB.update_name_product(product_id=product_id, new_name=message.text)
            await self.bot.send_message(chat_id=message.chat.id, text='Название товара успешно изменено!')
            await state.finish()

        @self.dp.message_handler(state=ProductChangeStatesGroup.price)
        async def change_name(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                product_id = data['product_id']
            self.DB.update_price_product(product_id=product_id, new_price=float(message.text))
            await self.bot.send_message(chat_id=message.chat.id, text='Цена товара успешно изменено!')
            await state.finish()

        @self.dp.message_handler(content_types='photo', state=ProductChangeStatesGroup.image)
        async def change_image(message: types.Message, state: FSMContext):
            print('image_handler')
            async with state.proxy() as data:
                product_id = data['product_id']
            image = message.photo[-1]
            image_p = io.BytesIO()
            await image.download(image_p)
            image_p.seek(0)
            new_image = image_p.getvalue()
            self.DB.update_image_product(product_id=product_id, new_image=new_image)
            await self.bot.send_message(chat_id=message.chat.id, text='Фото товара успешно изменено!')
            await state.finish()