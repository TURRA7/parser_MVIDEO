"""
Исполняющий модуль программы.

Func:

    monitoring_price: Функция мониторинга,
        раз в час проверяет актуальную цену на товар,
        добавляет её в базу данных.
    main: Создаёт таски, для асинхронного выполнения кода.
"""
import asyncio
import logging

from database.FDataBase import (get_session,
                                select_all_item,
                                add_item_price)
from backend.backend import get_html, get_price_item


logging.basicConfig(
    filename="CHECK_PRICE_API.log",
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def monitoring_price():
    """
    Функция мониторинга цены на товары.

    Notes:

        Получает асинхронную сессию aiohttp, в цикле while получает товары
        из базы данных если они есть, добавляет актуальную цену к каждому
        товару на мониторинге, далее функция засыпает на час, если товаров
        в базе нет, возвращает строку, говорящую об их отсутствии.
    """
    async for session in get_session():
        while True:
            products = await select_all_item(session=session)
            if isinstance(products, dict):
                products_list = products.get('message', [])
            else:
                logger.debug("Ошибка получения данных о товарах:", products)
                await asyncio.sleep(300)
                continue

            if not products_list:
                logger.debug("Отсутствуют товары для мониторинга!")
                await asyncio.sleep(300)
            else:
                if not all(isinstance(product,
                                      dict) for product in products_list):
                    logger.debug(
                        "Неправильный формат данных для 1/1+ товаров!")
                    await asyncio.sleep(300)
                    continue
                for product in products_list:
                    url_price = str(product['url_price'])
                    id_item = product['id']
                    data_html = await get_html(url=url_price)
                    data_price = await get_price_item(data_price=data_html)
                    if 'price' not in data_price:
                        logger.debug(data_price["error"])
                    else:
                        result = await add_item_price(product_id=int(id_item),
                                                      price=float(
                                                          data_price['price']),
                                                      session=session)
                        logger.debug(result["message"])
                await asyncio.sleep(3600)


async def main():
    monitoring_task = asyncio.create_task(monitoring_price())
    await monitoring_task


if __name__ == "__main__":
    asyncio.run(main())
