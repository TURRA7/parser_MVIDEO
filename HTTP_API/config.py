import os
from dotenv import load_dotenv

load_dotenv()

# Параметры подключения для базы данных PostgreSQL
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")

# Настройки приложения
SECRET_KEY = os.environ.get("SECRET_KEY")
