"""
Исполняющий модуль программы.

Func:

    main: Создаёт таблицы в базе данных.
"""
import asyncio
import uvicorn
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from database.FDataBase import create_tables
from routers.router import app_parsing
from config import SECRET_KEY


app = FastAPI()
app.include_router(app_parsing)
app.add_middleware(SessionMiddleware,
                   secret_key=SECRET_KEY,
                   max_age=360)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


logging.basicConfig(
    filename="HTTP_API.log",
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main() -> None:
    """
    Стартовая функция.

    func:
        create_tables: создаёт таблицы в базе.
    """
    try:
        await create_tables()
    except Exception as ex:
        logger.debug(ex)


if __name__ == "__main__":
    asyncio.run(main())
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
