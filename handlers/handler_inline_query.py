# import telebot.types
#
# from handlers.handler import Handler
# import os
# from settings.message import MESSAGES
# class HandlerInlineQuery(Handler):
#     def __init__(self, bot):
#         super().__init__(bot)
#         self.step = 0
#         self.message = None
#         self.isCall = False
#         print('777')
#     def pressed_btn_product(self, message, category, i = 0, previous_message = None):
#         pages_count = int(self.DB.select_count_products_in_category(category))
#         all_products_id = self.DB.select_all_products_id_in_category(category)
#         left = i - 1 if i != -1 else pages_count - 1
#         right = i + 1 if i != pages_count - 1 else 0
#         img_path = 'media/people_benzopyla.jpg'
#         image_file = open(img_path, 'rb')
#         image_data = image_file.read()
#         image_file.close()
#         name = self.DB.select_single_product_name(all_products_id[i])
#         price = self.DB.select_single_product_price(all_products_id[i])
#         quantity = self.DB.select_single_product_quantity(all_products_id[i])
#         if self.isCall == False:
#             print('00000')
#             self.isCall = True
#             self.message = self.bot.send_photo(message.chat.id, photo=image_data,
#                                         caption=f'{name}\nЦена: {price}\nКоличество на складе: {quantity}', reply_markup=self.keyboards.set_select_category(category, left, right, i, pages_count))
#
#         else:
#             self.bot.edit_message_media(message_id= message.message_id,chat_id = message.chat.id, media=telebot.types.InputMedia(type='photo', media=image_data,caption=f'{name}\nЦена: {price}\nКоличество на складе: {quantity}'), reply_markup=self.keyboards.set_select_category(category, left, right, i, pages_count))
#             print('11111')
#
#         # try: self.bot.delete_message(message.chat.id, previous_message.id)
#         # except: pass
#
#
#     # def pressed_btn_product(self, call):
#     #     if call.data == 'BACK_STEP':
#     #         img_path = 'media/people_benzopyla.jpg'
#     #         image_file = open(img_path, 'rb')
#     #         image_data = image_file.read()
#     #         image_file.close()
#     #         name = self.DB.select_single_product_name(code+1)
#     #         price = self.DB.select_single_product_price(code+1)
#     #         quantity = self.DB.select_single_product_quantity(code+1)
#     #         self.bot.send_photo(call.from_user.id, photo=image_data,
#     #                             caption=f'{name}\nЦена: {price}\nКоличество на складе: {quantity}')
#     #
#     #     elif call.data == 'NEXT_STEP':
#     #         img_path = 'media/people_benzopyla.jpg'
#     #         image_file = open(img_path, 'rb')
#     #         image_data = image_file.read()
#     #         image_file.close()
#     #         name = self.DB.select_single_product_name(code)
#     #         price = self.DB.select_single_product_price(code)
#     #         quantity = self.DB.select_single_product_quantity(code)
#     #         self.bot.send_photo(call.from_user.id, photo=image_data,
#     #                             caption=f'{name}\nЦена: {price}\nКоличество на складе: {quantity}')
#     #
#     #     elif call.data == 'ADD_TO_ORDER':
#     #         self.DB._add_orders(1, code, 1)
#     #         self.bot.answer_callback_query(call.id,
#     #                                        MESSAGES['product_order'].format(
#     #                                            self.DB.select_single_product_name(code),
#     #                                            self.DB.select_single_product_price(code),
#     #                                            self.DB.select_single_product_quantity(code)),
#     #                                        show_alert=True)
#     #
#     #
#     #     print(os.getcwd())
#     #     img_path = 'media/people_benzopyla.jpg'
#     #     image_file = open(img_path, 'rb')
#     #     image_data = image_file.read()
#     #     image_file.close()
#     #     name = self.DB.select_single_product_name(code)
#     #     price = self.DB.select_single_product_price(code)
#     #     quantity = self.DB.select_single_product_quantity(code)
#     #     self.bot.send_photo(call.from_user.id, photo=image_data,
#     #                         caption=f'{name}\nЦена: {price}\nКоличество на складе: {quantity}')
#
#     def handle(self):
#         @self.bot.callback_query_handler(func=lambda call: True)
#         def callback_inline(call):
#             if 'to' in call.data:
#                 page = int(call.data.split('_')[1])
#                 category = call.data.split('_')[2]
#                 self.pressed_btn_product(call.message, category, i=page, previous_message=call.message)
#             elif call.data == 'add':
#                 self.DB._add_orders(1, 1, 1)
#                 self.bot.answer_callback_query(call.id,
#                     MESSAGES['product_order'].format(self.DB.select_single_product_name(), self.DB.select_single_product_price(),self.DB.select_single_product_quantity()),show_alert=True)
#
#             # products_in_current_category = self.DB.select_all_products_category(call.data.split('|')[1])
#             # print('sadasdasd')
#             # if call.data.split('|')[0] == 'BACK_STEP':
#             #     print('----4')
#             #     self.step -= 1
#             #     print('----5')
#             #     img_path = 'media/people_benzopyla.jpg'
#             #     print('----3')
#             #     image_file = open(img_path, 'rb')
#             #     print('----2')
#             #     image_data = image_file.read()
#             #     print('----1')
#             #     image_file.close()
#             #     print('----')
#             #     name = self.DB.select_single_product_name(products_in_current_category[self.step].id)
#             #     print(name + "name")
#             #     price = self.DB.select_single_product_price(products_in_current_category[self.step].id)
#             #     quantity = self.DB.select_single_product_quantity(products_in_current_category[self.step].id)
#             #     self.bot.edit_message_media(media = telebot.types.InputMedia(type='photo', media=image_data, caption=f'{name}\nЦена: {price}\nКоличество на складе: {quantity}', message_id=call.message.message_id))
#             #
#             # elif call.data == 'NEXT_STEP':
#             #     self.step += 1
#             #
#             #     img_path = 'media/people_benzopyla.jpg'
#             #     image_file = open(img_path, 'rb')
#             #     image_data = image_file.read()
#             #     image_file.close()
#             #     name = self.DB.select_single_product_name(products_in_current_category[self.step])
#             #     price = self.DB.select_single_product_price(products_in_current_category[self.step])
#             #     quantity = self.DB.select_single_product_quantity(products_in_current_category[self.step])
#             #     self.bot.edit_message_media(media=telebot.types.InputMedia(type='photo', media=image_data,
#             #                                                                caption=f'{name}\nЦена: {price}\nКоличество на складе: {quantity}',
#             #                                                                chat_id=call.message.chat.id,
#             #                                                                message_id=call.message.message_id))
#             #
#             # elif call.data == 'ADD_TO_ORDER':
#             #     self.DB._add_orders(1, 1, 1)
#             #     self.bot.answer_callback_query(call.id,
#             #                                    MESSAGES['product_order'].format(
#             #                                        self.DB.select_single_product_name(),
#             #                                        self.DB.select_single_product_price(),
#             #                                        self.DB.select_single_product_quantity()),
#             #                                    show_alert=True)
#
#
