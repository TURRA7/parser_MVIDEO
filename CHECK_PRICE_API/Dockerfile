FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

COPY . .

CMD ["./wait-for-it.sh", "async_app:8000", "--timeout=15", "--strict", "--", "python", "main.py"]
