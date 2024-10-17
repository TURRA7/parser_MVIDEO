"""
Моудль логики парсинга товаров в магазине МВИДЕО.

Func:

    get_html: Получает на вход url (данные полученые от API магазина),
        возвращает спарсенные данные(dict).

    get_price_item: Получает на вход спарсенные данные(dict),
        возвращает цену товара(float).
"""
import json
import aiohttp


async def get_html(url: str) -> dict:
    """
    Функция получения данных с HTML страницы.

    Args:

        url: URL адресс товара.

    Returns:

        Возвращает словарь с данными сайта(МВИДЕО).
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 "
            "Mobile Safari/537.36"),
        "Cookie": ("MVID_CITY_ID=CityCZ_975; "
                   "MVID_REGION_ID=1; MVID_REGION_SHOP=S002; "
                   "MVID_TIMEZONE_OFFSET=3;")
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status in [401, 403]:
                return {
                    'error': f"Проблема авторизации, код: {response.status}"}
            elif response.status == 200:
                text = await response.text()
                return {"message": json.loads(text), "status_code": 200}
            else:
                return {'error': "Неверный формат ссылки!"}


async def get_price_item(data_price: dict) -> dict:
    """
    Функция поиска цены продукта.

    Args:

        data_price: Словарь с данными о цене(страница с API).

    Returns:

        Возвращает словарь с ценой товара.

    Notes:

        По наблюдениям, есть опасения, что ключи могут меняться.
    """
    if not isinstance(data_price, dict):
        return {'error': "Переданные данные, не являются словарем!",
                "status_code": 422}
    elif 'message' not in data_price:
        return {'error': "Отсутствует необходимый ключ 'message'.",
                "status_code": 422}
    elif "salePrice" not in (data_price['message']
                                       ["body"]["materialPrices"]
                                       [0]["price"]):
        return {'error': "Отсутствует необходимые ключи данных о товаре.",
                "status_code": 422}
    else:
        return {"price": (data_price['message']
                                    ["body"]
                                    ["materialPrices"]
                                    [0]["price"]["salePrice"]),
                "status_code": 200}
