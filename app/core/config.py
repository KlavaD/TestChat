from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Тестовое задание: Простой мессенджер'
    app_description: str = (
        '''
        Ваша задача - написать RESTful API простого мессенджера.
        Реализуемый функционал:
        - Механизм авторизации
        - Поиск пользователей
        - Возможность отправлять личные сообщения
        - Настройки пользователя (username, аватар, номер телефона, т.п.)
        '''
    )
    database_url: str = 'mongodb://localhost:27017'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()
