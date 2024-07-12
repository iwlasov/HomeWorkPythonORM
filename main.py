import sqlalchemy
import json
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Stock, Shop, Sale

if __name__ == '__main__':

    sqlsystem = 'postgresql'
    login = 'postgres'
    password = 'b2u18'
    host = 'localhost'
    port = 5432
    db_name = 'netology_db'

    DSN = f'{sqlsystem}://{login}:{password}@{host}:{port}/{db_name}'
    engine = sqlalchemy.create_engine(DSN)
    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    with open('fixtures/tests_data.json', 'r') as fd:
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

    search = input('Введите имя или идентификатор издателя: ')

    # result = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(Sale)
    result = session.query(Book).with_entities(Book.title, Shop.name, Sale.price, Sale.date_sale) \
        .join(Publisher, Publisher.id == Book.id_publisher) \
        .join(Stock, Stock.id_book == Book.id) \
        .join(Shop, Shop.id == Stock.id_shop) \
        .join(Sale, Sale.id_stock == Stock.id)

    # if search.isdigit():
    if search.isnumeric():
        result = result.filter(Publisher.id == search).all()
    else:
        result = result.filter(Publisher.name == search).all()

    for book_title, shop_name, sale_price, sale_date in result:
        # print(book_title, shop_name, sale_price,sale_date)
        print(f'{book_title: <50} | {shop_name: <30} | {sale_price: <10} | {sale_date}')

    session.close()