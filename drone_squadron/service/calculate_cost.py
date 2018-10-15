from crud.price_crud import PriceCrud


def calculate_cost(data):
    item_types = ('weapon', 'gimbal', 'scanner', 'thruster', 'steering')
    price = PriceCrud()
    cost = 0
    for item_type in item_types:
        if item_type in data:
            price = price.select_by_type_and_related_id(item_type, data.get(item_type))
            item = price.fetchone()
            if item:
                cost = cost + item.scrap
    return cost
