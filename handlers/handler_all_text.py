from aiogram.dispatcher import FSMContext

from settings import config, utility
from handlers.handler import Handler
from settings.message import MESSAGES
from aiogram import types, utils
import io
from PIL import Image

from states.states import ProductChangeStatesGroup, CreateProductStatesGroup, SearchUserById


class HandlerAllText(Handler):

    def __init__(self, bot, dp):
        super().__init__(bot, dp)
        # self.step = 0
        self.step_admin = 0
        self.isPaginationChooseCall = False
        self.isPaginationProductsAdminCall = False
        self.isPaginationCartCall = False
        self.isPaginationUserInfo = False
        self.isPaginationUserOrderInfo = False

    async def send_info_product(self, message_id, chat_id, category_id, i=0):
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
            await self.bot.send_photo(chat_id=chat_id, photo=image_bytes,
                                      caption=product_info_message,
                                      reply_markup=self.keyboards.set_select_category(category_id, left, right,
                                                                                      i,
                                                                                      pages_count))
        else:
            try:
                await self.bot.edit_message_media(message_id=message_id, chat_id=chat_id,
                                                  media=types.InputMediaPhoto(type='photo', media=image_bytes,
                                                                              caption=product_info_message),
                                                  reply_markup=self.keyboards.set_select_category(category_id,
                                                                                                  left, right,
                                                                                                  i, pages_count))
            except utils.exceptions.MessageNotModified:
                pass

    async def pressed_btn_category_admin(self, message_id, chat_id, category):
        self.step_admin = 0
        self.isPaginationProductsAdminCall = False
        all_products_id_in_category = self.DB.select_all_products_id_in_category(config.CATEGORY[category])
        await self.send_info_product_admin(all_products_id_in_category[self.step_admin], message_id, chat_id, category)

    async def send_info_product_admin(self, product_id, message_id, chat_id, category):
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
                await self.bot.edit_message_media(message_id=message_id, chat_id=chat_id,
                                                  media=types.InputMedia(type='photo', media=image_bytes,
                                                                         caption=msg, parse_mode="HTML"),
                                                  reply_markup=self.keyboards.change_menu_admin(self.step_admin,
                                                                                                quantity,
                                                                                                category,
                                                                                                product_id))
            except utils.exceptions.MessageNotModified:
                pass

    async def pressed_btn_category(self, message_id, chat_id, user_id, product_id):
        await self.bot.send_message(chat_id=chat_id, text='Категория:  ' + config.KEYBOARD[product_id])
        self.isPaginationChooseCall = False
        await self.send_info_product(message_id=message_id, chat_id=chat_id, category_id=config.CATEGORY[product_id])
        await self.bot.send_message(chat_id=chat_id, text='Выберите товар...',
                                    reply_markup=self.keyboards.category_menu(user_id))

    async def pressed_btn_choose_category(self, chat_id, user_id):
        await self.bot.send_message(chat_id=chat_id, text='Выберите категорию товара...',
                                    reply_markup=self.keyboards.category_menu(user_id))

    async def pressed_btn_info(self, chat_id):
        await self.bot.send_message(chat_id=chat_id, text=MESSAGES['trading_store'], parse_mode="HTML",
                                    reply_markup=self.keyboards.info_menu())

    async def pressed_btn_settings(self, chat_id):
        await self.bot.send_message(chat_id=chat_id, text=MESSAGES['settings'], parse_mode="HTML",
                                    reply_markup=self.keyboards.settings_menu())

    async def pressed_btn_back(self, chat_id):
        await self.bot.send_message(chat_id=chat_id, text="Вы вернулись в главное меню",
                                    reply_markup=self.keyboards.start_menu())

    async def pressed_btn_back_admin(self, chat_id):
        await self.bot.send_message(chat_id=chat_id, text="Вы вернулись в главное меню",
                                    reply_markup=self.keyboards.start_admin_menu())

    async def pressed_btn_shopping_cart(self, message_id, chat_id, user_id):
        # self.step = 0
        self.isPaginationCartCall = False
        all_products_id_in_order_by_user = self.DB.select_all_products_id_in_order_by_user(user_id)
        await self.send_info_products_in_order(message_id, chat_id,
                                               user_id)
        await self.bot.send_message(chat_id=chat_id,
                                    text='Можете отредактировать заказ или сразу перейти к оплате 😃',
                                    reply_markup=self.keyboards.payment_menu())

    async def send_info_products_in_order(self, message_id, chat_id, user_id, current_product_index=0, isAdmin=False):
        all_products_id_in_order = self.DB.select_all_products_id_in_order_by_user(user_id=user_id)
        if current_product_index > len(all_products_id_in_order) - 1:
            current_product_index = len(all_products_id_in_order) - 1
        elif current_product_index < 0:
            current_product_index = 0
        current_product = all_products_id_in_order[current_product_index]
        name, price, quantity = self.DB.select_single_product_info_in_shopping_cart(current_product, user_id)
        msg = MESSAGES['order_info'].format(current_product_index + 1, name, price, quantity, user_id)
        img_path = self.DB.select_single_product_image_path(current_product)

        with open(img_path, "rb") as file:
            image = Image.open(file)
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="JPEG")
            image_bytes.seek(0)
        if not isAdmin:
            if not self.isPaginationCartCall:
                self.isPaginationCartCall = True
                await self.bot.send_photo(chat_id=chat_id, photo=image_bytes,
                                          caption=msg, parse_mode="HTML",
                                          reply_markup=self.keyboards.orders_menu(current_product_index, quantity,
                                                                                  user_id))
            else:
                try:
                    print(chat_id)
                    await self.bot.edit_message_media(message_id=message_id, chat_id=chat_id,
                                                      media=types.InputMedia(type='photo', media=image_bytes,
                                                                             caption=msg, parse_mode="HTML"),
                                                      reply_markup=self.keyboards.orders_menu(current_product_index,
                                                                                              quantity,
                                                                                              user_id))
                except utils.exceptions.MessageNotModified:
                    pass
        else:
            if not self.isPaginationUserOrderInfo:
                self.isPaginationUserOrderInfo = True
                await self.bot.send_photo(chat_id=chat_id, photo=image_bytes,
                                          caption=msg, parse_mode="HTML",
                                          reply_markup=self.keyboards.orders_menu(current_product_index, quantity,
                                                                                  user_id))
            else:
                try:
                    await self.bot.edit_message_media(message_id=message_id, chat_id=chat_id,
                                                      media=types.InputMedia(type='photo', media=image_bytes,
                                                                             caption=msg, parse_mode="HTML"),
                                                      reply_markup=self.keyboards.orders_menu(current_product_index,
                                                                                              quantity, user_id))
                except utils.exceptions.MessageNotModified:
                    pass
    async def pressed_btn_up(self, message_id, chat_id, user_id, current_product_index, is_admin=False):
        count = self.DB.select_all_products_id_in_order_by_user(user_id)
        quantity_order = self.DB.select_quantity_product_in_order(count[current_product_index], user_id)
        print(quantity_order)
        quantity_product = self.DB.select_single_product_quantity(count[current_product_index])
        if quantity_product > 0:
            quantity_product -= 1
            quantity_order += 1
            self.DB.update_product_value(count[current_product_index], 'quantity', quantity_product)
            self.DB.update_order_value(count[current_product_index], user_id, 'quantity', quantity_order)
        await self.send_info_products_in_order(message_id, chat_id, user_id,
                                               current_product_index=current_product_index, isAdmin=is_admin)

    async def pressed_btn_up_admin(self, message_id, chat_id, category):
        all_products_id_in_category = self.DB.select_all_products_id_in_category(config.CATEGORY[category])
        product_id = all_products_id_in_category[self.step_admin]
        quantity_product = self.DB.select_single_product_quantity(product_id)
        if quantity_product > 0:
            quantity_product += 1
            self.DB.update_product_value(product_id, 'quantity', quantity_product)
        await self.send_info_product_admin(product_id, message_id, chat_id, category)

    async def pressed_btn_down(self, message_id, chat_id, user_id, current_product_index, is_admin=False):
        count = self.DB.select_all_products_id_in_order_by_user(user_id)
        quantity_order = self.DB.select_quantity_product_in_order(count[current_product_index], user_id)
        quantity_product = self.DB.select_single_product_quantity(count[current_product_index])
        if quantity_order > 1:
            quantity_order -= 1
            quantity_product += 1
            self.DB.update_order_value(count[current_product_index], user_id, 'quantity', quantity_order)
            self.DB.update_product_value(count[current_product_index], 'quantity', quantity_product)
        await self.send_info_products_in_order(message_id, chat_id, user_id,
                                               current_product_index=current_product_index, isAdmin=is_admin)

    async def pressed_btn_down_admin(self, message_id, chat_id, category):
        all_products_id_in_category = self.DB.select_all_products_id_in_category(config.CATEGORY[category])
        product_id = all_products_id_in_category[self.step_admin]
        quantity_product = self.DB.select_single_product_quantity(product_id)
        if quantity_product > 0:
            quantity_product -= 1
            self.DB.update_product_value(product_id, 'quantity', quantity_product)
        await self.send_info_product_admin(product_id, message_id, chat_id, category)

    async def pressed_btn_delete_product_admin(self, product_id, category, message_id, chat_id, call_id):
        if self.DB.check_product_in_order(product_id):
            await self.bot.answer_callback_query(call_id, MESSAGES['product_delete_prohibition'], show_alert=True)
        else:
            self.DB.delete_product(product_id)
            await self.bot.answer_callback_query(call_id, MESSAGES['product_delete_successfully'], show_alert=True)
            self.step_admin = 0
            all_products_id_in_category = self.DB.select_all_products_id_in_category(config.CATEGORY[category])
            await self.send_info_product_admin(all_products_id_in_category[self.step_admin], message_id, chat_id,
                                               category)

    async def pressed_btn_delete_product(self, message_id, chat_id, user_id, current_product_index, is_admin=False):
        all_products_id = self.DB.select_all_products_id_in_order_by_user(user_id)
        if all_products_id.__len__() > 0:
            quantity_order = self.DB.select_quantity_product_in_order(all_products_id[current_product_index], user_id)
            quantity_product = self.DB.select_single_product_quantity(all_products_id[current_product_index])
            quantity_product += quantity_order
            self.DB.delete_order(all_products_id[current_product_index], user_id)
            self.DB.update_product_value(all_products_id[current_product_index], 'quantity', quantity_product)
            current_product_index -= 1
            if current_product_index < 0:
                current_product_index = 0
        all_products_id = self.DB.select_all_products_id_in_order_by_user(user_id)
        if all_products_id.__len__() > 0:
            await self.send_info_products_in_order(message_id, chat_id, user_id,
                                                   current_product_index=current_product_index, isAdmin=is_admin)
        else:
            await self.bot.send_message(chat_id, MESSAGES['no_orders'], parse_mode='HTML',
                                        reply_markup=self.keyboards.category_menu(user_id))
            await self.bot.send_sticker(user_id, sticker='CAACAgIAAxkBAAEItpdkRufWmhez95pjUQ085yEuMyB3gQACXhYAAgthsUoLzhboOivPfC8E')


    async def pressed_btn_previous_product_admin(self, message_id, chat_id, category):
        if self.step_admin > 0:
            self.step_admin -= 1
        elif self.step_admin == 0:
            self.step_admin = self.DB.count_rows_products_in_category(config.CATEGORY[category]) - 1
        all_products_id_in_category = self.DB.select_all_products_id_in_category(config.CATEGORY[category])
        await self.send_info_product_admin(all_products_id_in_category[self.step_admin], message_id, chat_id, category)


    async def pressed_btn_next_step_admin(self, message_id, chat_id, category):
        if self.step_admin < self.DB.count_rows_products_in_category(config.CATEGORY[category]) - 1:
            self.step_admin += 1
        else:
            self.step_admin = 0
        all_products_id_in_category = self.DB.select_all_products_id_in_category(config.CATEGORY[category])
        await self.send_info_product_admin(all_products_id_in_category[self.step_admin], message_id, chat_id, category)

    async def pressed_btn_apply(self, chat_id, user_id, first_name, last_name, username):
        total_cost = utility.get_total_coast(self.DB, user_id)

        self.DB.add_user_info(user_id, first_name, last_name,
                              '@' + username)
        price = types.LabeledPrice(label="Оплата товара", amount=int(total_cost)*100)
        await self.bot.send_invoice(chat_id,
                               title="Товары ГИКMERCH",
                               description="Оплата товаров",
                               provider_token=config.PAYMENT_TOKEN,
                               currency="rub",
                               photo_url="https://phonoteka.org/uploads/posts/2021-05/1621807146_14-phonoteka_org-p-gik-fon-16.jpg",
                               photo_width=416,
                               photo_height=234,
                               photo_size=416,
                               is_flexible=False,
                               prices=[price],
                               start_parameter="one-month-subscription",
                               payload="test-invoice-payload")
        # client = self.DB.select_user(user_id)
        # order_info = str(client) + utility.get_all_information_user_order(self.DB, user_id)
        # await self.bot.send_message(config.ADMIN_ID, text=order_info, parse_mode="HTML")

    async def send_info_users_admin(self, chat_id, page=0, message_id=0):
        users = self.DB.select_all_users()
        if page > len(users) - 1:
            page = len(users) - 1
        elif page < 0:
            page = 0
        current_user = users[page]
        if not self.isPaginationUserInfo:
            await self.bot.send_message(chat_id=chat_id, text=str(current_user), parse_mode='HTML',
                                        reply_markup=self.keyboards.users_info_menu_admin(page, len(users)))
            self.isPaginationUserInfo = True
        else:
            try:
                await self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=str(current_user),
                                                 parse_mode='HTML',
                                                 reply_markup=self.keyboards.users_info_menu_admin(page, len(users)))
            except utils.exceptions.MessageNotModified:
                pass

    async def handle(self):
        @self.dp.message_handler(lambda message: message.from_user.id != config.ADMIN_ID)
        async def handle(message: types.Message):
            print('=0p09=--=')
            if message.text == config.KEYBOARD['INFO']:
                await self.pressed_btn_info(message.chat.id)
            elif message.text == config.KEYBOARD['SETTINGS']:
                await self.pressed_btn_settings(message.chat.id)
            elif message.text == config.KEYBOARD['<<']:
                await self.pressed_btn_back(message.chat.id)
            elif message.text == config.KEYBOARD['CHOOSE_GOODS']:
                await self.pressed_btn_choose_category(message.chat.id, message.from_user.id)
            elif message.text == config.KEYBOARD['ORDER']:
                if self.DB.count_rows_order(message.from_user.id) > 0:
                    await self.pressed_btn_shopping_cart(message.message_id, message.chat.id, message.from_user.id)
                else:
                    await self.bot.send_message(chat_id=message.chat.id, text=MESSAGES['no_orders'], parse_mode="HTML",
                                                reply_markup=self.keyboards.category_menu(message))
                    await self.bot.send_sticker(message.from_user.id,
                                                sticker='CAACAgIAAxkBAAEItpdkRufWmhez95pjUQ085yEuMyB3gQACXhYAAgthsUoLzhboOivPfC8E')

            elif message.text == config.KEYBOARD['CLOTH']:
                await self.pressed_btn_category(message.message_id, message.chat.id, message.from_user.id, 'CLOTH')
            elif message.text == config.KEYBOARD['FIGURINES']:
                await self.pressed_btn_category(message.message_id, message.chat.id, message.from_user.id,
                                                'FIGURINES')
            elif message.text == config.KEYBOARD['MUGS']:
                await self.pressed_btn_category(message.message_id, message.chat.id, message.from_user.id, 'MUGS')
            elif message.text == config.KEYBOARD['APPLY']:
                await self.pressed_btn_apply(message.chat.id, message.from_user.id, message.from_user.first_name,
                                             message.from_user.last_name, message.from_user.username)

        #
        @self.dp.callback_query_handler(
            lambda call: call.from_user.id != config.ADMIN_ID and not call.data.startswith('change_order'))
        async def callback_inline(call: types.CallbackQuery):
            # is_order_present = self.DB.check_order_present(call.from_user.id)
            print('sadasd')
            if 'to' in call.data:
                page = int(call.data.split('_')[1])
                category_id = call.data.split('_')[2]
                await self.send_info_product(call.message.message_id, call.message.chat.id, category_id, i=page)
            elif 'add' in call.data:
                page = int(call.data.split('_')[1])
                category_id = call.data.split('_')[2]
                all_products_id = self.DB.select_all_products_id_in_category(category_id)
                product_id = all_products_id[page]
                self.DB.add_order(1, product_id, call.from_user.id)
                name, price, quantity = self.DB.select_single_product_info(product_id)
                add_product_message = MESSAGES['product_order'].format(name, price, quantity)
                await self.bot.answer_callback_query(call.id, add_product_message, show_alert=True)
                await self.send_info_product(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                             category_id=category_id, i=page)

        @self.dp.message_handler(lambda message: message.from_user.id == config.ADMIN_ID)
        async def admin_message_handler(message: types.Message):
            if message.text == config.KEYBOARD['SHOW_INFO_ORDERS']:
                self.isPaginationUserInfo = False
                await self.send_info_users_admin(message.chat.id)
            elif message.text == config.KEYBOARD['CHANGE_PRODUCTS']:
                await self.pressed_btn_choose_category(message.chat.id, message.from_user.id)
            elif message.text == config.KEYBOARD['<<']:
                await self.pressed_btn_back_admin(message.chat.id)
            elif message.text == config.KEYBOARD['CLOTH']:
                await self.pressed_btn_category_admin(message.message_id, message.chat.id, 'CLOTH')
            elif message.text == config.KEYBOARD['FIGURINES']:
                await self.pressed_btn_category_admin(message.message_id, message.chat.id, 'FIGURINES')
            elif message.text == config.KEYBOARD['MUGS']:
                await self.pressed_btn_category_admin(message.message_id, message.chat.id, 'MUGS')

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

        @self.dp.message_handler(state=CreateProductStatesGroup.name)
        async def add_name_product(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['product_name'] = message.text
            await self.bot.send_message(chat_id=message.chat.id, text='Введите цену нового товара...')
            await CreateProductStatesGroup.price.set()

        @self.dp.message_handler(state=CreateProductStatesGroup.price)
        async def add_price_product(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['product_price'] = float(message.text)
            await self.bot.send_message(chat_id=message.chat.id, text='Введите количество нового товара...')
            await CreateProductStatesGroup.quantity.set()

        @self.dp.message_handler(state=CreateProductStatesGroup.quantity)
        async def add_quantity_product(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['product_quantity'] = int(message.text)
            await self.bot.send_message(chat_id=message.chat.id, text='Отправьте изображение нового товара...')
            await CreateProductStatesGroup.image.set()

        @self.dp.message_handler(content_types='photo', state=CreateProductStatesGroup.image)
        async def add_image_product(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                category_id = config.CATEGORY[data['category']]
                product_name = data['product_name']
                product_price = data['product_price']
                product_quantity = data['product_quantity']
            image = message.photo[-1]
            image_p = io.BytesIO()
            await image.download(image_p)
            image_p.seek(0)
            new_image = image_p.getvalue()
            self.DB.add_product(category_id=self.DB.select_category(category_id), name=product_name,
                                price=product_price, quantity=product_quantity, image_bytes=new_image)
            await self.bot.send_message(chat_id=message.chat.id, text='Товар успешно добавлен!')
            await state.finish()

        @self.dp.message_handler(state=SearchUserById.user_id)
        async def add_quantity_product(message: types.Message, state: FSMContext):
            user_id = int(message.text)
            is_user_exist = self.DB.user_exists(user_id)
            if is_user_exist:
                await self.bot.send_message(chat_id=message.chat.id, text='Данные заказа пользователя')
                await self.send_info_products_in_order(message_id=message.message_id, chat_id=message.chat.id, user_id=user_id, isAdmin=True)
            else:
                await self.bot.send_message(chat_id=message.chat.id, text='Пользователь отсутвует в базе(...')
            await state.finish()
        @self.dp.callback_query_handler(lambda call: call.data and call.data.startswith('change_order'))
        async def changes_order_callback_query_handler(call: types.CallbackQuery):
            print('eq=w0e=-0')
            user_id = call.data.split('_')[5]
            is_order_present = self.DB.check_order_present(user_id)
            is_admin = call.from_user.id == config.ADMIN_ID
            if 'down_count' in call.data:
                if is_order_present:
                    await self.pressed_btn_down(call.message.message_id, call.message.chat.id, user_id,
                                                int(call.data.split('_')[4]), is_admin=is_admin)
                else:
                    await self.bot.answer_callback_query(call.id, MESSAGES['no_orders'], show_alert=True)

            elif 'up_count' in call.data:
                if is_order_present:
                    print(int(call.data.split('_')[4]))
                    await self.pressed_btn_up(call.message.message_id, call.message.chat.id, user_id,
                                              int(call.data.split('_')[4]), is_admin=is_admin)
                else:
                    await self.bot.answer_callback_query(call.id, MESSAGES['no_orders'], show_alert=True)

            elif 'back_product' in call.data:
                if is_order_present:
                    print(int(call.data.split('_')[4]))
                    await self.send_info_products_in_order(call.message.message_id, call.message.chat.id,
                                                           user_id, current_product_index=int(call.data.split('_')[4]),
                                                           isAdmin=is_admin)
                else:
                    await self.bot.answer_callback_query(call.id, MESSAGES['no_orders'], show_alert=True)
            elif 'next_product' in call.data:
                if is_order_present:
                    print(int(call.data.split('_')[4]))
                    await self.send_info_products_in_order(call.message.message_id, call.message.chat.id, user_id,
                                                           current_product_index=int(call.data.split('_')[4]),
                                                           isAdmin=is_admin)
                else:
                    await self.bot.answer_callback_query(call.id, MESSAGES['no_orders'], show_alert=True)
            elif 'delete_product' in call.data:
                if is_order_present:
                    await self.pressed_btn_delete_product(call.message.message_id, call.message.chat.id,
                                                          user_id, int(call.data.split('_')[4]), is_admin=is_admin)
                else:
                    await self.bot.answer_callback_query(call.id, MESSAGES['no_orders'], show_alert=True)

        @self.dp.callback_query_handler(
            lambda call: call.from_user.id == config.ADMIN_ID and not call.data.startswith(
                'change') and not call.data.startswith('add_product'))
        async def admin_callback_query_handler(call: types.CallbackQuery):
            print('][][]]]')
            if 'up_product_count' in call.data:
                await self.pressed_btn_up_admin(call.message.message_id, call.message.chat.id, call.data.split('_')[3])

            elif 'down_product_count' in call.data:
                await self.pressed_btn_down_admin(call.message.message_id, call.message.chat.id,
                                                  call.data.split('_')[3])

            elif 'next_product' in call.data:
                await self.pressed_btn_next_step_admin(call.message.message_id, call.message.chat.id,
                                                       call.data.split('_')[2])

            elif 'back_product' in call.data:
                await self.pressed_btn_previous_product_admin(call.message.message_id, call.message.chat.id,
                                                              call.data.split('_')[2])
            elif 'delete_product' in call.data:
                await self.pressed_btn_delete_product_admin(call.data.split('_')[2], call.data.split('_')[3],
                                                            call.message.message_id, call.message.chat.id, call.id)
            elif 'back_user' in call.data:
                await  self.send_info_users_admin(call.message.chat.id, int(call.data.split('_')[2]),
                                                  call.message.message_id)
            elif 'next_user' in call.data:
                await  self.send_info_users_admin(call.message.chat.id, int(call.data.split('_')[2]),
                                                  call.message.message_id)
            elif 'choose_user' in call.data:

                await self.send_info_products_in_order(call.message.message_id, call.message.chat.id,
                                                       int(call.data.split('_')[2]),
                                                       isAdmin=True)
                self.isPaginationUserOrderInfo = True
            elif 'search_user' in call.data:
                await self.bot.send_message(chat_id=call.message.chat.id, text='Напишите id пользователя...')
                await SearchUserById.user_id.set()
        @self.dp.callback_query_handler(
            lambda call: call.from_user.id == config.ADMIN_ID and not call.data.startswith(
                'change_order') and not call.data.startswith('add_product'))
        async def pressed_btn_change_name_product(call: types.CallbackQuery, state: FSMContext):
            product_id = call.data.split('_')[2]
            print('==-=-=-')
            async with state.proxy() as data:
                data['product_id'] = product_id

            await self.bot.send_message(chat_id=call.message.chat.id, text='Введите новое значение...')

            if 'change_name' in call.data:
                await ProductChangeStatesGroup.name.set()
            elif 'change_price' in call.data:
                await ProductChangeStatesGroup.price.set()
            elif 'change_image' in call.data:
                print('change_image')
                await ProductChangeStatesGroup.image.set()

        @self.dp.callback_query_handler(lambda call: call.data and call.data.startswith('add_product'))
        async def pressed_btn_add_product(call: types.CallbackQuery, state: FSMContext):
            print('12312314')
            category = call.data.split('_')[2]
            async with state.proxy() as data:
                data['category'] = category
            await self.bot.send_message(chat_id=call.message.chat.id, text='Введите имя нового товара...')
            await CreateProductStatesGroup.name.set()

        @self.dp.pre_checkout_query_handler(lambda query: True)
        async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
            await self.bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

        # successful payment
        @self.dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
        async def successful_payment(message: types.Message):
            print("SUCCESSFUL PAYMENT:")
            payment_info = message.successful_payment.to_python()
            for k, v in payment_info.items():
                print(f"{k} = {v}")

            await self.bot.send_message(message.chat.id,
                                   f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")
            client = self.DB.select_user(message.from_user.id)
            order_info = str(client) + utility.get_all_information_user_order(self.DB, message.from_user.id)
            await self.bot.send_message(config.ADMIN_ID, text=order_info, parse_mode="HTML")
            total_cost = utility.get_total_coast(self.DB, message.from_user.id)
            total_quantity = utility.get_total_quantity(self.DB, message.from_user.id)
            apply_message = MESSAGES['apply'].format(message.from_user.id, total_cost, total_quantity)
            await self.bot.send_sticker(message.from_user.id,
                                        sticker='CAACAgIAAxkBAAEItp1kRuhZE8GR5q1NHmvqvVrI1MeAJwACwhUAAlAdSUhTlP1Qw1XqOC8E')
            await self.bot.send_message(message.chat.id, apply_message, parse_mode='HTML',
                                        reply_markup=self.keyboards.category_menu(message.from_user.id))
