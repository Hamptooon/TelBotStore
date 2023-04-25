from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from settings import config
from data_base.dbalchemy import DBManager

class Admin_Keyboards:
    def __init__(self):
        self.markup = None
        self.DB = DBManager()

    def set_btn(self, name):
        return KeyboardButton(config.KEYBOARD[name])