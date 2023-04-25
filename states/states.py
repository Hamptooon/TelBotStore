from aiogram.dispatcher.filters.state import StatesGroup, State


class ProductChangeStatesGroup(StatesGroup):
    product_id = State()
    name = State()
    price = State()
    image = State()


class CreateProductStatesGroup(StatesGroup):
    category = State()
    name = State()
    price = State()
    quantity = State()
    image = State()

class SearchUserById(StatesGroup):
    user_id = State()
