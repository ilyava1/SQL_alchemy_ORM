import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, sessionmaker
import models
import os
import dotenv
import service

if __name__ == '__main__':

    dotenv.load_dotenv('config.env')
    DBMS = os.getenv('DBMS')
    DB_NAME = os.getenv('DB_NAME')
    DB_LOGIN = os.getenv('DB_LOGIN')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    SERVER = os.getenv('SERVER')
    PORT = os.getenv('PORT')
    DB_CONTENT_FILE = os.getenv('DB_CONTENT_FILE')

    print()
    print('Из файла конфигурации "config.env" в переменные окружения загружены'
          ' следующие настройки:')
    print(' - DBMS: ', DBMS)
    print(' - DB_NAME: ', DB_NAME)
    print(' - DB_LOGIN: ', DB_LOGIN)
    print(' - DB_PASSWORD: **********')
    print(' - SERVER: ', SERVER)
    print(' - SERVER PORT: ', PORT)
    print(' - Файл с контентом для БД: ', DB_CONTENT_FILE)
    print()
    choice = input('Продолжить с этими настройками - Enter, '
                   'Выход - любая клавиша + Enter ')
    if choice != '':
        exit()

    Base = declarative_base()

    DSN = (DBMS + '://' + DB_LOGIN + ':'
                  + DB_PASSWORD + '@' + SERVER
                  + ':' + PORT + '/' + DB_NAME)

    engine = sq.create_engine(DSN)
    models.create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    service.insert_data(session)

    service.search_for_shops(session)
