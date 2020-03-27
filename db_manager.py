import sqlite3
import os


def extract(lst):
    return list(map(lambda el: el[0], lst))


class SQLighter:

    def __init__(self):
        self.db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tgShopBase.db')
        try:
            with sqlite3.connect(self.db_file) as db:
                dbcursor = db.cursor()
                dbcursor.execute("""CREATE TABLE "store_articles" (
                                    "article_id"	INTEGER NOT NULL UNIQUE,
                                    "sort"	TEXT NOT NULL,
                                    "description"	TEXT,
                                    "availability"	INTEGER NOT NULL,
                                    "amount"	INTEGER NOT NULL,
                                    "price"	NUMERIC NOT NULL,
                                    PRIMARY KEY("article_id")
                                ),  CREATE TABLE "new_orders" (
	                                "order_id"	INTEGER NOT NULL UNIQUE,
                                    "customer_id"	INTEGER NOT NULL,
                                    "article"	INTEGER NOT NULL,
                                    "amount"	INTEGER NOT NULL,
                                    PRIMARY KEY("order_id")
                                ),  CREATE TABLE "customers" (
                                    "customer_id"	INTEGER NOT NULL UNIQUE,
                                    "customer_name"	TEXT ,
                                    "phone"	TEXT UNIQUE,
                                    "delivery_adress" TEXT,
                                    PRIMARY KEY("customer_id")
                                )""")
                db.commit()
        except sqlite3.OperationalError:
            pass

###################################################ARTICLES HANDLING####################################################

    def load_all_articles(self):
        with sqlite3.connect(self.db_file) as db:
            return [[str(j) for j in i] for i in db.cursor().execute('SELECT * FROM store_articles', ).fetchall()]

    def add_new_article(self, article_id, sort, description, availability, amount, price):
        with sqlite3.connect(self.db_file) as db:
            db.cursor().execute(
                'INSERT INTO store_articles (article_id, sort, description, availability, amount, price) VALUES (?, ?, ?, ?, ?, ?)',
                (article_id, sort, description, availability, amount, price))
            db.commit()

    def update_article(self, article_id, sort, description, availability, amount, price):
        with sqlite3.connect(self.db_file) as db:
            db.cursor().execute(
                'UPDATE store_articles SET sort = (?), description = (?), availability = (?), amount = (?), price = (?) WHERE article_id = (?)',
                (sort, description, availability, amount, price, article_id))
            db.commit()

    def is_sort_in_table(self, sort):
        with sqlite3.connect(self.db_file) as db:
            return True if extract(db.cursor().execute('SELECT EXISTS (SELECT * FROM store_articles WHERE sort = (?))',
                                                    (sort, )).fetchall()) else False

    def delete_article(self, article_id):
        with sqlite3.connect(self.db_file) as db:
            db.cursor().execute("DELETE FROM store_articles WHERE article_id = (?)", (article_id,))
            db.commit()

####################################################ORDERS HANDLING#####################################################

    def load_all_orders(self):
        with sqlite3.connect(self.db_file) as db:
            return [[str(j) for j in i] for i in db.cursor().execute('SELECT * FROM new_orders', ).fetchall()]

###################################################СUSTOMERS HANDLING###################################################

    def create_new_customer(self, customer_id):
        with sqlite3.connect(self.db_file) as db:
            db.cursor().execute(
                'INSERT INTO сustomers (customer_id,) VALUES (?, )', (customer_id, ))
            db.commit()

    def get_customer_by_id(self, customer_id):
        with sqlite3.connect(self.db_file) as db:
            return [[str(j) for j in i] for i in db.cursor().execute('SELECT * FROM customers WHERE customer_id = (?)', (customer_id,)).fetchall()]

    def update_customer(self, customer_id, customer_name, phone, delivery_address):
        with sqlite3.connect(self.db_file) as db:
            db.cursor().execute(
                'UPDATE customers SET customer_name = (?), phone = (?), delivery_address = (?) WHERE article_id = (?)',
                (customer_name, phone, delivery_address, customer_id, ))
            db.commit()
