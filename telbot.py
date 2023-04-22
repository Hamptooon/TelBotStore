from settings import config
from handlers.handler_main import HandlerMain
# from telebot import TeleBot
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio


class TelBot:
    __version__ = config.VERSION
    __author__ = config.AUTHOR

    def __init__(self):
        self.storage = MemoryStorage()
        self.token = config.TOKEN
        self.bot = Bot(self.token)
        self.dp = Dispatcher(self.bot, storage=self.storage)
        self.handler = HandlerMain(self.bot, self.dp)

    async def start(self):
        await self.handler.handle()

    def run_bot(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.start())
        executor.start_polling(self.dp, loop=loop, skip_updates=True, )


if __name__ == '__main__':
    bot = TelBot()
    bot.run_bot()
