from emoji import emojize
from .config import KEYBOARD, VERSION, AUTHOR

trading_store = f"""<b>{emojize(':fire:')}ДОБРО ПОЖАЛОВАТЬ В КОНЕЧНЫЙ ПУНКТ НАЗНАЧЕНИЯ ДЛЯ ВСЕГО ГИКОВСКОГО И КРУТОГО!{emojize(':fire:')}</b>

<b>{emojize(':joystick:')} ГИКmerch</b> - это страна чудес для <i>коллекционеров</i>, <i>энтузиастов</i> и <i>суперфанатов</i>, предлагающая широкий ассортимент уникальных и захватывающих продуктов, <i>которые обязательно заставят ваше сердце биться чаще</i>. От замысловато детализированных игрушек и фигурок, которые захватывают каждую деталь ваших любимых персонажей, до стильной одежды, которая позволяет вам с гордостью <b>демонстрировать свой фандом</b>, у нас есть все!. Наш выбор кружек и других товаров для дома идеально подходит для того, чтобы добавить нотку гик-шика в вашу повседневную жизнь!{emojize(':star_struck:')}

Независимо от того, являетесь ли вы ярым поклонником комиксов, научно-фантастических фильмов, видеоигр или чего-то среднего, у нас вы найдете что-то для себя. <i><b>Так что приходите и исследуйте нашу удивительную коллекцию товаров сегодня!</b></i>{emojize(':collision:')}"""

settings = """
<b>Общее руководство ботом:</b>

<i>Навигация:</i>

-<b>({}) - </b><i>назад</i>
-<b>({}) - </b><i>вперед</i>
-<b>({}) - </b><i>увеличить</i>
-<b>({}) - </b><i>уменьшить</i>
-<b>({}) - </b><i>следующий</i>
-<b>({}) - </b><i>предыдующий</i>

<i>Специальные кнопки:</i>

-<b>({}) - </b><i>удалить</i>
-<b>({}) - </b><i>заказ</i>
-<b>({}) - </b><i>Оформить заказ</i>

<i>Общая информация:</i>

-<b>версия программы: - </b><i>({})</i>
-<b>разработчик: - </b><i>({})</i>


<b>{}ГИК.merch</b>

""".format(
    KEYBOARD['<<'],
    KEYBOARD['>>'],
    KEYBOARD['UP'],
    KEYBOARD['DOWN'],
    KEYBOARD['NEXT_STEP'],
    KEYBOARD['BACK_STEP'],
    KEYBOARD['X'],
    KEYBOARD['ORDER'],
    KEYBOARD['APPLY'],
    VERSION,
    AUTHOR,
    KEYBOARD['COPY'],
)
product_order = """
Выбранный товар:

{}
Cтоимость: {} руб

Добавлен в заказ!!!

На складе осталось {} ед. 
"""
# order = """
#
# <i>Название:</i> <b>{}</b>
#
# <i>Cтоимость:</i> <b>{} руб за 1 ед.</b>
#
# <i>Количество позиций:</i> <b>{} ед.</b>
# """
#
# order_number = """
#
# <b>Позиция в заказе № </b> <i>{}</i>
#
# """
order_info = """
<b>Позиция в заказе № </b> <i>{}</i>

<i>Название:</i> <b>{}</b>

<i>Cтоимость:</i> <b>{} руб за 1 ед.</b>

<i>Количество позиций:</i> <b>{} ед.</b> 
"""
no_orders = """
Заказ отсутствует !!!
"""

apply = """
<b>Ваш заказ оформлен 🥰!!!</b>

<b><i>Номер заказа: </i></b> #{}

<i>Общая стоимость заказа 💰:</i> <b>{} руб </b>

<i>Количество товаров в заказе:</i> <b>{} ед.</b>

<b>ЗАКАЗ НАПРАВЛЕН НА СКЛАД 😄!</b>


p.s для уточнения информации о заказе обратитесь сюда 🧙‍♂️: @pixxxiz 
"""
product_delete_prohibition = """
Товар не может быть удален, так как пристувует в заказе
"""
product_delete_successfully = """
Товар удален из базы
"""
hello_message = """
{}, здравствуйте ! Жду дальнейших указаний 🤩
"""
user_order_info = """
<b>💸 Заказ оплачен 💸</b>

{}

Информация о заказе:


"""
MESSAGES = {
    'hello_message': hello_message,
    'trading_store': trading_store,
    'product_order': product_order,
    'order_info': order_info,
    # 'order': order,
    # 'order_number': order_number,
    'no_orders': no_orders,
    'apply': apply,
    'settings': settings,
    'product_delete_prohibition': product_delete_prohibition,
    'product_delete_successfully': product_delete_successfully
}
