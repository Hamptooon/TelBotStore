import os
from emoji import emojize
TOKEN = '5819700782:AAH7MqXb3_CevbScYXzU8kxZZIUiYYlucdo'
NAME_DB = 'products.db'
VERSION = '0.0.1'
AUTHOR = 'User'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join('sqlite:///' + BASE_DIR, NAME_DB)
COUNT = 0
KEYBOARD = {
    'CHOOSE_GOODS': emojize(':open_file_folder: Выбрать товар'),
    'INFO': emojize(':speech_balloon: О магазине'),
    'SETTINGS': emojize('⚙️ Настройки'),
    'CLOTH': emojize(':kimono: Одежда'),
    'FIGURINES': emojize(':robot: Фигурки'),
    'MUGS': emojize(':hot_beverage: Кружки'),
    '<<': emojize('⏪'),
    '>>': emojize('⏩'),
    'BACK_STEP': emojize('◀️'),
    'NEXT_STEP': emojize('▶️'),
    'ORDER': emojize('✅ ЗАКАЗ'),
    'X': emojize('❌'),
    'DOWN': emojize('🔽'),
    'AMOUNT_PRODUCT': COUNT,
    'AMOUNT_ORDERS': COUNT,
    'UP': emojize('🔼'),
    'APPLY': '✅ Оформить заказ',
    'COPY': '©️'
}
CATEGORY = {
    'CLOTH': 1,
    'FIGURINES': 2,
    'MUGS': 3,
}
COMMANDS = {
    'START': "start",
    'HELP': "help",
}

MESSAGES = {}
