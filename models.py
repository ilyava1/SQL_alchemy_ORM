import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    def __str__(self):
        return f'id: {self.id}, {self.name}'

    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)


class Book(Base):
    def __str__(self):
        return f'id: {self.id}, {self.title}, ' \
               f'id издательства - {self.id_publisher}'

    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.Text, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"
                                                       ), nullable=False)

    publisher = relationship(Publisher, backref="books")


class Shop(Base):
    def __str__(self):
        return f'id: {self.id}, {self.name}'

    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)


class Stock(Base):
    def __str__(self):
        return f'id: {self.id}, id книги: {self.id_book}, ' \
               f'id магазина: {self.id_shop}, кол-во экз.: {self.count}'

    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    book = relationship(Book, backref="stocks")
    shop = relationship(Shop, backref="shops")


class Sale(Base):
    def __str__(self):
        return f'id: {self.id}, цена - {self.book_pr} руб., ' \
               f'дата - {self.date_sale}, id запаса - {self.id_stock}, ' \
               f'участвует в распродаже - {self.count} шт.'

    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    book_pr = sq.Column(sq.Numeric, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"),
                         nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship(Stock, backref="sales")


def create_tables(engine):
    drop_tables(engine)
    Base.metadata.create_all(engine)
    print()
    print('Созданы таблицы БД:')
    for i in Base.metadata.tables.keys():
        print(f' - {i}')
    print()


def drop_tables(engine):
    Base.metadata.drop_all(engine)
    print('Таблицы БД удалены')
    print()
