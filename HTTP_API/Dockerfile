FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

COPY . .

EXPOSE 8000

CMD ["./wait-for-it.sh", "db:5432", "--timeout=10", "--strict", "--", "python", "main.py"]