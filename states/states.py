from aiogram.dispatcher.filters.state import StatesGroup, State


class ProductChangeStatesGroup(StatesGroup):
    product_id = State()
    name = State()
    price = State()
    image = State()