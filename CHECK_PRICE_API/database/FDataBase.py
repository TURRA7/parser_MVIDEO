"""
Модуль для работы с базой данных.

Models:

    Product: Содержит основную инфу о товаре:
        id, название, описание, рейтинг,
        URL на API с основными данными,
        URL на API с данными о цене.
        Так же связь с таблицей истории цен.

    PriceHistory: Содержит:
        id записи, id товара к которому она прикреплена,
        цена на товар, время добавления цены, а так же связь
        с таблицей информации о продукте.

Func:

    get_session: Создаёт асинхронную сессию,
        для работы с базой данных

    select_all_item: Возвращает все товары,
        находящиеся в базе(на мониторинге)

    add_item_price: Получает на вход:
        id продукта, цену, объект сессии,
        возвращает актуальную цену на товар(float).
"""
from typing import AsyncGenerator
from sqlalchemy import (Column, DateTime, ForeignKey,
                        Integer, String, Float, select)
from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession)
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase
from sqlalchemy import func

from config import (DB_USER, DB_PASS, DB_HOST, DB_NAME)

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


class Product(Base):
    """
    Таблица с общей информацией о продукте.

    Args:

        id: id товара.
        name: Название товара.
        description: Описание товара.
        rating: Рейтинг товара.
        url_info: Ссылка на API с общей информацией о товаре.
        url_price: Ссылка на API с информацией о цене товара.
        price_history: Связь с таблицей истории цен на товар.
    """
    __tablename__ = "products"
    

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    rating = Column(Float)
    url_info = Column(String, nullable=False)
    url_price = Column(String, nullable=False)

    price_history = relationship("PriceHistory",
                                 back_populates="product",
                                 cascade="all, delete")


class PriceHistory(Base):
    """
    Таблица истории цен на товары.

    Args:

        id: id записи.
        product_id: id продукта.
        price: Цена продукта.
        timestamp: Время добавления цены.
        product: Связь с таблицей общей информации о продукте.
    """
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=func.now())

    product = relationship("Product", back_populates="price_history")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Функция получения асинхронной сессии."""
    async with AsyncSessionLocal() as session:
            yield session


async def select_all_item(
        session: AsyncSession) -> dict:
    """
    Функция получения товаров на мониторинге.

    Args:

        session: Асинхронная сессия для базы данных.
    
    Returns:

        Возвращает список(словарь) товаров, находящихся на мониторинге
    """
    try:
        result = await session.scalars(select(Product))
        products = [{"id": res.id, "name": res.name,
                    "description": res.description,
                    "rating": round(res.rating, 1),
                    "url_info": res.url_info,
                    "url_price": res.url_price} for res in result]
        return {"message": products, "status_code": 200}
    except Exception as ex:
        return {"message": f"Ошибка получения товаров на мониторинге: {ex}",
                "status_code": 422}


async def add_item_price(product_id: int, price: float,
                         session: AsyncSession) -> bool:
    """
    Функция добавления цены на товар.

    Args:

        product_id: id товара, к которому добавляется цена
        price: Цена на товар.
        session: Асинхронная сессия для базы данных.
    
    Returns:
        Добавляет цену к товару в базе данных,
        возвращает сообщение об успехе или ошибке и статус кода.
    """
    result = PriceHistory(product_id=product_id, price=price)
    try:
        session.add(result)
        await session.commit()
        return {"message": f"Цена {price} добавленa: {product_id}",
                "status_code": 200}
    except Exception as ex:
        return {"message": f"Проблемы с добавлением цены: {ex}",
                "status_code": 422}
