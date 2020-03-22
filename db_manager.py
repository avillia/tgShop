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
                                )""")
                db.commit()
        except sqlite3.OperationalError:
            pass

########################################################################################################################

    def load_all_articles(self):
        with sqlite3.connect(self.db_file) as db:
            dbcursor = db.cursor()
            return [[str(j) for j in i] for i in dbcursor.execute('SELECT * FROM store_articles', ).fetchall()]

    def add_new_article(self, article_id, sort, description, availability, amount, price):
        with sqlite3.connect(self.db_file) as db:
            dbcursor = db.cursor()
            dbcursor.execute(
                'INSERT INTO store_articles (article_id, sort, description, availability, amount, price) VALUES (?, ?, ?, ?, ?, ?)',
                (article_id, sort, description, availability, amount, price))
            db.commit()

    def update_article(self, article_id, sort, description, availability, amount, price):
        with sqlite3.connect(self.db_file) as db:
            dbcursor = db.cursor()
            dbcursor.execute(
                'UPDATE store_articles SET sort = (?), description = (?), availability = (?), amount = (?), price = (?) WHERE article_id = (?)',
                (sort, description, availability, amount, price, article_id))
            db.commit()

    def is_sort_in_table(self, sort):
        with sqlite3.connect(self.db_file) as db:
            dbcursor = db.cursor()
            return True if extract(dbcursor.execute('SELECT EXISTS (SELECT * FROM store_articles WHERE sort = (?))',
                                                    (sort, )).fetchall()) else False

    def delete_article(self, article_id):
        with sqlite3.connect(self.db_file) as db:
            dbcursor = db.cursor()
            dbcursor.execute("DELETE FROM store_articles WHERE article_id = (?)", (article_id,))
            db.commit()
