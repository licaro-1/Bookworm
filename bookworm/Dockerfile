FROM python:3.11-slim
LABEL authors="licaro"

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn","bookworm.wsgi:application","--bind","0:8000"]