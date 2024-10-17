"""
Моудль логики парсинга товаров в магазине МВИДЕО.

Func:

    get_html: Получает на вход url (данные полученые от API магазина),
        возвращает спарсенные данные(dict).

    get_info_item: Получает на вход спарсенные данные(dict), возвращает:
        название товара, описание товара и рейтинг товара.
"""
import json
import aiohttp


class ParseHTMLError(Exception):
    """Вызывается при ошибочной ссылки/ошибках '401' или '403'."""
    pass


class ParseINFOError(Exception):
    """Вызывается при неверно переданных данных/отсутствием заданных ключей."""
    pass


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
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile "
            "Safari/537.36"
        ),
        "Cookie": (
            "MVID_CITY_ID=CityCZ_975; MVID_REGION_ID=1; "
            "MVID_REGION_SHOP=S002; MVID_TIMEZONE_OFFSET=3;"
        )
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


async def get_info_item(data_info: dict) -> dict:
    """
    Функция поиска информации о продукте.

    Args:

        data_info: Словарь с данными о товаре(страница с API).

    Returns:

        Возвращает словарь с общей информацией о товаре.
    """
    if not isinstance(data_info, dict):
        return {'error': "Переданные данные, не являются словарем!",
                "status_code": 422}
    elif 'body' not in data_info:
        return {'error': "Отсутствует необходимый ключ 'body'.",
                "status_code": 422}
    elif 'name' not in data_info['body']:
        return {'error': "Отсутствует необходимые ключи данных о товаре.",
                "status_code": 422}
    else:
        return {"name": data_info['body']['name'],
                "description": data_info['body']['description'],
                "rating": data_info['body']['rating']['star'],
                "status_code": 200}
