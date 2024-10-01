import os
from dotenv import load_dotenv

load_dotenv()

# Параметры подключения к базе данных.
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
