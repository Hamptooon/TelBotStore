def _convert(list_convert):
    return [itm[0] for itm in list_convert]
def total_coast(all_quantity, all_price):
    order_total_coast = 0
    for index, itm in enumerate(all_price):
        order_total_coast += all_price[index]*all_quantity[index]
    return order_total_coast
def total_quantity(all_quantity):
    return sum(all_quantity)
def get_total_coast(DB):
    all_products_id = DB.select_all_products_id()
    all_price = [DB.select_single_product_price(itm) for itm in all_products_id]
    all_quantity = [DB.select_order_quantity(itm) for itm in all_products_id]
    return total_coast(all_quantity, all_price)

def get_total_quantity(DB):
    all_products_id = DB.select_all_products_id()
    all_quantity = [DB.select_order_quantity(itm) for itm in all_products_id]
    return total_quantity(all_quantity)