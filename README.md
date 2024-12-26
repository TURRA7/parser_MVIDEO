# Тестовое задание

---

### **Технологии:**
- **FastAPI**
- **Docker-compose**
- **PostgreSQL**
- **SQLAlchemy**

---

### **Задача:** *Реализовать микросервисное веб-приложение для мониторинга цен на любом сайте (например, М.Видео).*

---

### **Необходимо предусмотреть следующий функционал:**

1. **Модуль HTTP API** с использованием библиотеки **FastAPI**.  
   Должен содержать следующие маршруты:
   - Добавление нового товара на мониторинг (ссылка на товар).
   - Удаление товара.
   - Получение списка товаров на мониторинге.
   - Получение истории цен на товар.

2. **Telegram бот** с аналогичным функционалом.

3. **Модуль мониторинга**, который будет периодически получать новую цену товара:
   - При добавлении товара необходимо получать только его название, описание и рейтинг (если есть).
   - Получать информацию можно через библиотеку `requests`.
   - Записывать цену на товар необходимо **раз в час**.

4. **База данных** для хранения информации (**PostgreSQL**).

---

### **Важные моменты:**
- Запуск кода через **docker-compose**, каждый модуль в отдельном контейнере.
- Модуль базы данных должен иметь **volume** для сохранения информации.
- Для работы с базой использовать библиотеку **SQLAlchemy**.
- (Опционально) Добавить странички для маршрутов бэкенда с помощью шаблонов Jinja2, стилизовав их с использованием Bootstrap.

---

## **Инструкция**

---

### **Первичная подготовка:**

1. В Telegram обратитесь к боту [@BotFather](https://t.me/BotFather) и создайте нового бота:
   - Получите у него **токен**.
   - Сразу отправьте созданному боту любое сообщение (**это важно!**).

2. В Telegram обратитесь к боту [@getmyid_bot](https://t.me/getmyid_bot):
   - Отправьте ему любое сообщение.
   - Получите ваш **ID**.

3. Для данных PostgreSQL:
   1. Установите PostgreSQL, скачав его с [официального сайта](https://www.postgresql.org/).
   2. После установки откройте консоль и выполните:  
      ```bash
      sudo -u postgres psql
      ```
   3. В консоли PostgreSQL создайте базу данных:
      ```sql
      CREATE DATABASE mydatabase;
      ```
   4. Создайте пользователя:
      ```sql
      CREATE USER myuser WITH PASSWORD 'mypassword';
      ```
   5. Выдайте права пользователю:
      ```sql
      GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
      ```

---

### **Основная настройка и старт:**

1. Откройте каталог **testovoe** в вашем **IDE** или через **bash**.

2. В файле **docker-compose.yaml** вместо конструкций `"${...значение...}"` укажите:
   - Укажите параметры согласно комментариям.
   - **Важно:** оставьте строку `DB_HOST: "db"` без изменений.
   - В сервисе **aiogram_bot** добавьте ваши данные:
     - Параметр **TOKEN** — токен, полученный у [@BotFather](https://t.me/BotFather).
     - Параметр **ADMIN_ID** — ID, полученный у [@getmyid_bot](https://t.me/getmyid_bot).

3. В каталоге проекта выполните команду:
   ```bash
   docker-compose up --build
