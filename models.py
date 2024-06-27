import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

#1. Составить модели классов SQLAlchemy

class Publisher(Base):
    __tablename__ = 'publisher'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=100), unique=True)
    # def __str__(self):
        # return f'{self.id}: {self.name}'

class Book(Base):
    __tablename__ = 'book'
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=255), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)
    # def __str__(self):
        # return f'{self.id}, {self.title}, {self.id_publisher}'

    publisher = relationship(Publisher, backref='book') #связь с книги с авторами

class Shop(Base):
    __tablename__ = 'shop'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=60), unique=True)
    # def __str__(self):
        # return f'{self.id}: {self.name}'

class Stock(Base):
    __tablename__ = 'stock'
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer)
    # def __str__(self):
        # return f'{self.id}, id книги - {self.id_book}, id магазина - {self.shop}, количество книг в магазине - {self.count}'

    book = relationship(Book, backref='stock') #связь с таблицей книги
    shop = relationship(Shop, backref='stock') #связь с таблицей магазины

class Sale(Base):
    __tablename__ = 'sale'
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer)
    # def __str__(self):
        # return f'{self.id}, цена - {self.price}, дата продажи - {self.date_sale}, id запаса - {self.id_stock}, количество проданных книг - {self.count}'

    stock = relationship(Stock, backref='sale') #связь с таблицей магазинов

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

