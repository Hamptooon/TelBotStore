
def convert(list_convert):
    return [itm[0] for itm in list_convert]


def total_coast(all_quantity, all_price):
    order_total_coast = 0
    for index, itm in enumerate(all_price):
        order_total_coast += all_price[index] * all_quantity[index]
    return order_total_coast


def total_quantity(all_quantity):
    return sum(all_quantity)


def get_total_coast(DB, user_id):
    all_products_id = DB.select_all_products_id_in_order_by_user(user_id)
    all_price = [DB.select_single_product_price(itm) for itm in all_products_id]
    all_quantity = [DB.select_quantity_product_in_order(itm, user_id) for itm in all_products_id]
    return total_coast(all_quantity, all_price)


def get_total_quantity(DB, user_id):
    all_products_id = DB.select_all_products_id_in_order_by_user(user_id)
    all_quantity = [DB.select_quantity_product_in_order(itm, user_id) for itm in all_products_id]
    return total_quantity(all_quantity)
def get_all_information_user_order(DB, user_id):
    products_in_order = DB.select_user_order_info(user_id)
    info = """
🔎 <b>Информация о заказе</b>:
    
📜 <i>Список товаров</i>
"""
    for product_in_order in products_in_order:
        info += '<b>🔹 Название товара:</b> ' + str(DB.select_single_product_name(product_in_order.product_id)) + '\n\n'
        info += '<b>🔸 Цена: </b>' + str(DB.select_single_product_price(product_in_order.product_id)) + '\n\n'
        info += '<b>🔸 Количество в заказе:</b> ' + str(DB.select_quantity_product_in_order(product_in_order.product_id, user_id)) + '\n\n'
        info += '➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
    info += '<b>💰 СУММА ЗАКАЗА: ' + str(get_total_coast(DB, user_id)) + ' РУБ 💰</b>'
    return info
