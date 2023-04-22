import abc
from markup.markup import Keyboards
from data_base.dbalchemy import DBManager


class Handler(metaclass=abc.ABCMeta):

    def __init__(self, bot, dp):
        self.bot = bot
        self.dp = dp
        self.keyboards = Keyboards()
        self.DB = DBManager()

    @abc.abstractmethod
    async def handle(self):
        pass
