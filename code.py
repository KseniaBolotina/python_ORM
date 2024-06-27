import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale
import json
import os

db_user = os.getenv('db_user', 'postgres')
db_password = os.getenv('DB_PASSWORD', 'UhjvVjkybb1155+')
db_host = os.getenv('db_host', 'localhost')
db_port = os.getenv('db_port', '5432')
db_name = os.getenv('db_name', 'book')
DSN = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures/test_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

def find_publisher_info(publisher_input): # = input('Введите имя издателя: ')):
    if publisher_input.isdigit():
        find_info = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(
            Stock).join(Shop).join(Sale).filter(Publisher.id == publisher_input)
        for fp in find_info:
            print((f'{fp[0]} | {fp[1]} | {fp[2]} | {fp[3]}'))
    else:
        find_info = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(
            Stock).join(Shop).join(Sale).filter(Publisher.name.like(publisher_input))
        for f in find_info:
            print(f'{f[0]} | {f[1]} | {f[2]} | {f[3]}')

if __name__ == '__main__':
    publisher_input = input('Введите имя или идентификатор издателя: ')
    find_publisher_info(publisher_input)

session.close()