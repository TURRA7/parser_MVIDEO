"""
Модуль содержит обработчики(хендлеры aiogram3).

Func:

    fetch_data: Асинхронная сессия для отправки HTTP запроса.
    start_bot: Отправляет пользователю сообщение о старте бота.
    stop_bot: Отправляет пользователю сообщение об остановке бота.
    get_start: Старт работы с ботом. Реагирует на команду /start.

    send_instruction: Добавление товара на мониторинг. FSM первый этап.
    form_add_item: Добавление товара на мониторинг. FSM второй этап.
    form_url_price: Добавление товара на мониторинг. FSM третий этап.

    delete_step_one: Удаление товара с мониторинга. FSM первый этап.
    delete_step_two: Удаление товара с мониторинга. FSM второй этап.
    
    get_list_monitoring: Получение списка товаров на мониторинге.

    get_history_price_step_one: Получение истории цен на товар. FSM первый этап.
    get_history_price_step_two: Получение истории цен на товар. FSM второй этап.
"""
import os
import logging
import aiohttp
from aiogram import F
from datetime import datetime
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Bot, Router, types
from aiogram.fsm.context import FSMContext

from core.forms_state.form_bot import Form_add, Form_id_delete, Form_id_list
from core.keyboards.reply_inline import ReplyKeyBoards
from core.content.contents import messages, emoticons, url, instruction
from core.utils.commands import set_commands


logger = logging.getLogger(__name__)
admin_id = int(os.getenv('ADMIN_ID'))
router = Router()


async def fetch_data(url: str, method: str = "GET",
                     params: dict = None, data: dict = None) -> dict:
    """
    Асинхронная сессия для отправки HTTP запроса.

    Args:

        url: URL адрес для запроса.
        method: HTTP метод запроса.
        params: Параметры в запросе после знака '?'.
        data: JSON данные для запроса.
    
    Returns:

        Возвращает JSON данные в виде словаря с ответом от сервера.
    """
    async with aiohttp.ClientSession() as session:
        if method == 'GET':
            async with session.get(url, params=params) as response:
                return await response.json()
        elif method == 'POST':
            async with session.post(url, json=data) as response:
                return await response.json()
        elif method == 'DELETE':
            async with session.delete(url, json=data) as response:
                return await response.json()


async def start_bot(bot: Bot):
    """Отправляет пользователю сообщение о старте бота."""
    await set_commands(bot)
    await bot.send_message(admin_id, text=messages[1])
    logger.info("Бот запущен!")


async def stop_bot(bot: Bot):
    """Отправляет пользователю сообщение об остановке бота."""
    await bot.send_message(admin_id, text=messages[2])
    logger.info("Бот остановлен!")


@router.message(Command("start"))
async def get_start(message: Message):
    """
    Старт работы с ботом.

    Notes:
        При воде команды /start или при выборе её в меню,
        открывает стартовый интерфейс, для взаимодействия с ботом.
    """
    if message.from_user.id == admin_id:
        await message.answer(
            f"<b>{message.from_user.first_name}</b> <b>{messages[4]}</b>",
            reply_markup=ReplyKeyBoards.create_keyboard_reply(emoticons[1],
                                                              emoticons[2],
                                                              emoticons[3],
                                                              emoticons[4],
                                                              emoticons[5]))
    else:
        await message.answer(
            f"<b>{message.from_user.first_name}</b>{messages[1]}")


@router.message(F.text == emoticons[1], F.from_user.id == admin_id)
async def send_instruction(message: Message):
    """Отправляет пользователю инструкцию."""
    await message.answer(instruction[1])


@router.message(F.text == emoticons[2], F.from_user.id == admin_id)
async def form_add_item(message: Message, state: FSMContext):
    """
    Добавление товара на мониторинг. FSM первый этап.

    Notes:

        Включает форму Form_add, отправляет пользователю подсказки
    """
    await state.set_state(Form_add.url_info)
    await message.answer(messages[5])


@router.message(Form_add.url_info, F.from_user.id == admin_id)
async def form_url_info(message: Message, state: FSMContext):
    """
    Добавление товара на мониторинг. FSM второй этап.

    Notes:

        Фиксирует первую ссылку на товар,
        переходит к следующему состоянию формы,
        отправлет пользователю дальнейшие инструкции.
    """
    await state.update_data(url_info=message.text)
    await state.set_state(Form_add.url_price)
    await message.answer(messages[6])


@router.message(Form_add.url_price, F.from_user.id == admin_id)
async def form_url_price(message: Message, state: FSMContext):
    """
    Добавление товара на мониторинг. FSM третий этап.

    Notes:

        Фиксирует вторую ссылку на товар, получает сохраненные данные,
        отправляет запрос на сервер, возвращает пользователю ответ сервера,
        очищает состояния.
    """
    try:
        await state.update_data(url_price=message.text)
        data: dict = await state.get_data()
        response = await fetch_data(url=url['add'], method="POST", data=data)
        if 'detail' in response:
            error = response['detail'][0]
            await message.answer(
                "Укажите верный URL формата 'https://... как в инструкции!")
            logger.debug("Проблема с форматом введённой почты!")
        else:
            await message.answer(response['message'])
    except aiohttp.ClientError as ex:
        await message.answer("Ошибка соединения с сервером... Попробуйте позже.")
        logger.debug("Ошибка соединения %s", ex)
    except Exception as ex:
        await message.answer("Ошибка в работе бота... Попробуйте позже.")
        logger.debug("Ошибка проиложеиня %s", ex)
    finally:
        await state.clear()


@router.message(F.text == emoticons[3], F.from_user.id == admin_id)
async def delete_step_one(message: Message, state: FSMContext):
    """
    Удаление товара с мониторинга. FSM первый этап.

    Notes:

        Включает форму Form_id_delete, отправляет пользователю подсказки
    """
    await state.set_state(Form_id_delete.product_id)
    await message.answer(messages[7])


@router.message(Form_id_delete.product_id, F.from_user.id == admin_id)
async def delete_step_two(message: Message, state: FSMContext):
    """
    Удаление товара с мониторинга. FSM второй этап.

    Notes:

        Фиксирует id товара, получает сохраненные данные,
        отправляет запрос на сервер, возвращает пользователю ответ сервера,
        очищает состояния.
    """
    await state.update_data(product_id=int(message.text))
    data: dict = await state.get_data()
    try:
        delete_url = f"{url['delete']}/{data['product_id']}"
        response = await fetch_data(url=delete_url,
                                    method="DELETE")
        if 'detail' in response:
            error = response['detail'][0]
            await message.answer("Ошибка в работе бота... Попробуйте позже.")
            logger.debug("Ошибка добавления товара: type - %s msg - %s",
                         error['type'],
                         error['msg'])
        else:
            await message.answer(response['message'])
    except aiohttp.ClientError as ex:
        await message.answer("Ошибка соединения с сервером... Попробуйте позже.")
        logger.debug("Ошибка соединения %s", ex)
    except Exception as ex:
        await message.answer("Ошибка в работе бота... Попробуйте позже.")
        logger.debug("Ошибка проиложеиня %s", ex)
    finally:
        await state.clear()


@router.message(F.text == emoticons[4], F.from_user.id == admin_id)
async def get_list_monitoring(message: types.Message):
    """
    Получение списка товаров на мониторинге.

    Notes:

        Отправляет запрос на сервер на получение списка товаров,
        возвращает ответ пользователю.
    """
    try:
        response = await fetch_data(url=url['get_list'], method="GET")
        if response == None:
            await message.answer("Проблема в работе сервера... Попробуйте позже.")
            logger.debug("Проблема с работой сервера!.")
        products = response['message']
        if isinstance(products, list):
            for item in products:
                await message.answer(f"id: {item['id']}\n"
                                    f"name: {item['name']}\n"
                                    f"rating: {item['rating']}")
        else:
            await message.answer(text=products)
    except aiohttp.ClientError as ex:
        await message.answer("Ошибка соединения с сервером... Попробуйте позже.")
        logger.debug("Ошибка соединения %s", ex)
    except Exception as ex:
        await message.answer("Ошибка в работе бота... Попробуйте позже.")
        logger.debug("Ошибка проиложеиня %s", ex)


@router.message(F.text == emoticons[5], F.from_user.id == admin_id)
async def get_history_price_step_one(message: Message, state: FSMContext):
    """
    Получение истории цен на товар. FSM первый этап.

    Notes:

        Включает форму Form_id_list, отправляет пользователю подсказки
    """
    await state.set_state(Form_id_list.product_id)
    await message.answer(messages[7])


@router.message(Form_id_list.product_id, F.from_user.id == admin_id)
async def get_history_price_step_two(message: Message, state: FSMContext):
    """
    Получение истории цен на товар. FSM второй этап.

    Notes:

        Фиксирует id товара, получает сохраненные данные,
        отправляет запрос на сервер, возвращает пользователю ответ сервера,
        очищает состояния.
    """
    await state.update_data(product_id=int(message.text))
    data: dict = await state.get_data()
    try:
        get_list_url = f"{url['get_history']}/{data['product_id']}"
        response = await fetch_data(url=get_list_url,
                                    method="GET")
        if 'detail' in response:
            error = response['detail'][0]
            await message.answer("Ошибка в работе бота... Попробуйте позже.")
            logger.debug("Ошибка добавления товара: type - %s msg - %s",
                         error['type'],
                         error['msg'])
        else:
            history_price = response['message']
            if isinstance(history_price, list):
                for item in history_price:
                    time_obj = datetime.strptime(item['date'], "%Y-%m-%dT%H:%M:%S.%f")
                    form_time = time_obj.strftime("%d-%m-%Y %H:%M:%S")
                    await message.answer(f"ID товара: {item['product_id']}\n"
                                        f"Цена: {item['price']}\n"
                                        f"Дата добавления цены: {form_time}")
            elif isinstance(history_price, str):
                await message.answer(history_price)
    except aiohttp.ClientError as ex:
        await message.answer("Ошибка соединения с сервером... Попробуйте позже.")
        logger.debug("Ошибка соединения %s", ex)
    except Exception as ex:
        await message.answer("Ошибка в работе бота... Попробуйте позже.")
        logger.debug("Ошибка проиложеиня %s", ex)