<div align="center">

<p style="text-align:center;"><img style="text-align:center;" src="assets/logo_card.jpg" alt="logo"/></p>

### Bookworm - онлайн библиотека IT-книг с возможностью комментирования и их оценки.
</div>

[![tested](https://github.com/licaro-1/Bookworm/actions/workflows/main.yml/badge.svg?branch=main&event=push&job=tests)](https://github.com/licaro-1/Bookworm/actions/workflows/main.yml)

<details>
<summary style="font-size:25px; font-weight: bold;">Установка и запуск</summary>


1. Клонировать репозиторий
    ```bash
    git clone https://github.com/licaro-1/Bookworm.git
    ```

2. Перейти в склонированный репозиторий:
    ```bash
    cd ./Bookworm/
    ```

3. Создать виртуальное окружение и активировать его (Команды зависят от ОС)
    ```bash
    python -m venv venv
    ```
   ```bash
    . .\venv\Scripts\activate
    ```

4. Создать .env файл в директории infra и заполнить необходимые переменные из .env-example
    ```bash
    cd infra/
    ```
    ```bash
    touch .env
    ```

5. Установить зависимости
    ```bash
    pip install -r .\bookworm\requirements.txt
    ```


6. Создать файл nginx.prod.conf в директории infra/nginx 
и заполнить необходимой информацией по примеру nginx.prod.example.conf


7. Поднять docker контейнеры
   ```bash
      docker compose -f docker-compose.prod.yaml up --build
   ```

8. Запустить миграции и подгрузить статику
   ```python
   docker exec -it infra-web-1 python manage.py migrate
   docker exec -it infra-web-1 python manage.py collectstatic
   ```
9. Запустить тесты
   ```python
   docker exec -it infra-web-1 python manage.py tests
   ```
</details>




## Технологии:

--- 

* Django 5
* Loguru
* PostgreSQL
* Docker
* Selectel S3
* Nginx