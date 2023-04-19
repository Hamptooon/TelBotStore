import os
from emoji import emojize

TOKEN = '5819700782:AAH7MqXb3_CevbScYXzU8kxZZIUiYYlucdo'
PAYMENT_TOKEN = '1744374395:TEST:a85968c29c32f822bc4d'
ADMIN_ID = 5175787483
NAME_DB = 'products.db'
VERSION = '0.0.1'
AUTHOR = 'User'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join('sqlite:///' + BASE_DIR, NAME_DB)
COUNT = 0
KEYBOARD = {
    'CHOOSE_GOODS': emojize(':open_file_folder: Выбрать товар'),
    'INFO': emojize(':speech_balloon: О нас'),
    'SETTINGS': emojize('⚙️ Настройки'),
    'CLOTH': emojize(':kimono: Одежда'),
    'FIGURINES': emojize(':robot: Фигурки'),
    'MUGS': emojize(':hot_beverage: Кружки'),
    '<<': emojize('⏪'),
    '>>': emojize('⏩'),
    'BACK_STEP': emojize('◀️'),
    'ADD_TO_ORDER': emojize('Добавить в заказ'),
    'NEXT_STEP': emojize('▶️'),
    'ORDER': emojize('🛒 Корзина'),
    'X': emojize('❌'),
    'DOWN': emojize('🔽'),
    'AMOUNT_PRODUCT': COUNT,
    'AMOUNT_PRODUCTS': COUNT,
    'AMOUNT_ORDERS': COUNT,
    'UP': emojize('🔼'),
    'APPLY': '✅ Оплатить',
    'COPY': '©️',
    'CHANGE_PRODUCTS': '📕 Информация о товарах',
    'SHOW_INFO_ORDERS': '🔎 Информация о заказах',
    'MAIN_MENU': 'В главное меню',
    'CHANGE': 'Изменить...',
    'CHANGE_PHOTO': '📷 Фото',
    'CHANGE_PRICE': '💵 Цену',
    'CHANGE_NAME': '🏷️ Имя'

}
# ADMIN_KEYBOARD={
#     '':
# }
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
