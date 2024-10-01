"""
Модуль для работы с формами машины состояний FSM.

Classes:

    Form_add:
        url_info: URL адрес API МВИДЕО c основной инфо о товаре.
        url_price: URL адрес API МВИДЕО c инфо о цене товара.

    Form_id_delete:
        product_id: id товара в базе данных.
    
    Form_id_list:
        product_id: id товара в базе данных.
"""
from aiogram.fsm.state import State, StatesGroup


class Form_add(StatesGroup):
    """
    Форма для добавления товара в базу данных.

    Args:

        url_info: URL адрес API МВИДЕО c основной инфо о товаре.
        url_price: URL адрес API МВИДЕО c инфо о цене товара.
    """
    url_info = State()
    url_price = State()


class Form_id_delete(StatesGroup):
    """
    Форма для удаления товара из базы.

    Args:

        product_id: id товара в базе данных.
    """
    product_id = State()


class Form_id_list(StatesGroup):
    """
    Форма для получения истории цен на товар.

    Args:

        product_id: id товара в базе данных.
    """
    product_id = State()

