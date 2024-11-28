FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=api_gateway.settings 

EXPOSE 8001

CMD ["sh", "-c", "daphne -b 0.0.0.0 -p 8000 api_gateway.asgi:application"]
