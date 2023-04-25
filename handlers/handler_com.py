from handlers.handler import Handler
from settings import config
from settings.message import MESSAGES
from aiogram import types


class HandlerCommands(Handler):

    def __init__(self, bot, dp):
        super().__init__(bot, dp)

    async def pressed_btn_start(self, message):
        hello_message = MESSAGES['hello_message'].format(message.from_user.first_name)
        if message.from_user.id == config.ADMIN_ID:
            await self.bot.send_message(chat_id=message.chat.id, text=hello_message,
                                        reply_markup=self.keyboards.start_admin_menu())
        else:
            await self.bot.send_message(chat_id=message.chat.id, text=hello_message,
                                        reply_markup=self.keyboards.start_menu())
        await self.bot.send_sticker(message.from_user.id,
                                    sticker='CAACAgIAAxkBAAEItqVkRusN1tqC6Os6fx7oTwXQ8PvNnwACaxsAAh5daEs-Fz0zds-_9i8E')

    async def handle(self):
        @self.dp.message_handler(commands=['start'])
        async def handle(message: types.Message):
            if message.text == '/start':
                await self.pressed_btn_start(message)
