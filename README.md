# Тестовое задание: написать RESTful API простого мессенджера.
В данном проекте создана API для простого мессенджера. Регистрация пользователя, авторизация, отправка и получение сообщений.
Автор -
*   [Клавдия Дунаева](https://www.t.me/klodunaeva)


**Инструменты и стек:**-
* Python 3.11
* [FastAPI](https://fastapi.tiangolo.com/)
* [FastAPI-Users](https://fastapi-users.github.io/fastapi-users/10.0/)
* [MongoDB](https://www.mongodb.com/)
* [Pydantic](https://docs.pydantic.dev/latest/)
* [Docker Compose](https://docs.docker.com/compose/)



**Как запустить проект:**

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/KlavaD/TestChat.git
```

```
cd TestChat
```

Создать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

Обновить pip:

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Создать файл .env

```
APP_TITLE=
APP_DESCRIPTION=
DATABASE_URL='mongodb://localhost:27017'
SECRET=
FIRST_SUPERUSER_EMAIL=
FIRST_SUPERUSER_PASSWORD=
```
Запустите MongoDB в контейнере Docker:
Перейдите в папку infra и выполните команду:
```
docker compose up -d
```
Запустить FastAPI-сервер:
```
uvicorn main:app
```
Или запустите файл main.py

[Посмотреть документацию и выполнить тестовые запросы](http://127.0.0.1:8000/docs)
