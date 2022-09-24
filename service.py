import models
import json
import os


def insert_data(session):
    """
    Функция первичного наполнения таблиц БД

    Функция извлекает данные из json-файла и добавляет их в таблицы БД.
    Все добавленные записи по таблицам выводятся на экран
    :param session:
    :return: None
    """
    DB_CONTENT_FILE = os.getenv('DB_CONTENT_FILE')

    with open(DB_CONTENT_FILE, 'r', encoding='utf-8') as f:
        content = json.load(f)

    # Добавление издательств:
    print('Добавлены издательства: ')
    for value in content['publishers']:
        new_pub = models.Publisher(name=value)
        session.add(new_pub)
        session.commit()
        print(' - ', new_pub)
    print()

    # Добавление книг:
    print('Добавлены книги: ')
    for value in content['books']:
        new_book = models.Book(title=value[0], id_publisher=value[1])
        session.add(new_book)
        session.commit()
        print(' - ', new_book)
    print()

    # Добавление магазинов:
    print('Добавлены магазины: ')
    for value in content['shops']:
        new_shop = models.Shop(name=value)
        session.add(new_shop)
        session.commit()
        print(' - ', new_shop)
    print()

    # Добавление запасов
    print('Добавлены магазины: ')
    for value in content['stock']:
        new_stock = models.Stock(id_book=value[0], id_shop=value[1],
                                 count=value[2])
        session.add(new_stock)
        session.commit()
        print(' - ', new_stock)
    print()

    # Добавление распродаж
    print('Добавлены распродажи: ')
    for value in content['sales']:
        new_sale = models.Sale(book_pr=value[0], date_sale=value[1],
                               id_stock=value[2], count=value[3])
        session.add(new_sale)
        session.commit()
        print(' - ', new_sale)
    print()

    print('Загрузка начальных данных в БД завершена')
    print()

    return


def search_for_shops(session):
    """
    Функция поска магазинов продажи продукции целевого издательства

    Функция запрашивает идентификатор издательства, проверяет ввод пользова-
    теля на корректность - чтобы было введено целое число и чтобы идентифи-
    катор присутствовал в базе, - затем нахаодит магазин(ы), продающий
    продукцию издательства и выводит его данные на экран
    :param session:
    :return: None
    """
    while True:
        try:
            pub_id = int(input('Для поиска магазинов, продающих продукцию '
                               'определенного издательства, введите '
                               'идентификатор данного издательства: '))
        except ValueError:
            print('Небходимо ввести число')
            continue
        q = session.query(models.Publisher).filter(models.Publisher.id
                                                   == pub_id)
        result = q.all()
        if result == []:
            print('Издатель с таким идентификатором отсутствует в базе')
            print()
            continue
        print(f'Продукция издательства {result[0].name} продается в следующих'
              f' магазинах:')

        q = session.query(models.Shop).join(models.Stock.shop).join(
            models.Book).join(models.Publisher).filter(models.Publisher.id
                                                       == pub_id)

        result = q.all()
        for i in result:
            print(' - ', i)

        return
