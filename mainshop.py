from flask import Flask, render_template, request, jsonify, url_for
from db_manager import *


class Article:
    def __init__(self, id, sort, description, availability, amount, price):
        self.id = id
        self.sort = sort
        self.description = description
        self.availability = availability
        self.amount = amount
        self.price = price


class Order:
    def __init__(self, id, customer, article, amount):
        self.id = id
        self.customer = customer
        self.article = article
        self.amount = amount


app = Flask(__name__)
db = SQLighter()


@app.route('/')
def main_page():
    return render_template('mainshop.html', name="SampleShop")


@app.route('/store')
def store_page():
    return render_template('store.html', name="SampleShop", articles=[Article(*i) for i in db.load_all_articles()])


@app.route('/orders')
def orders_page():
    return render_template('orders.html', name="SampleShop", articles=[Article(*i) for i in db.load_all_articles()])


@app.route('/sql', methods=['PATCH'])
def sql_update():
    json = {"error": None}
    try:
        db.update_article(article_id=request.args["article_id"],
                          sort=request.args["sort"],
                          description=request.args["description"],
                          availability=request.args["availability"],
                          amount=request.args["amount"],
                          price=request.args["price"])
        return 'Existing article successfully updated.', 200
    except sqlite3.IntegrityError as E:
        json["error"] = repr(E)
        return jsonify(json), 500


@app.route('/sql', methods=['POST'])
def sql_add():
    json = {"error": None}
    try:
        db.add_new_article(article_id=request.args["article_id"],
                           sort=request.args["sort"],
                           description=request.args["description"],
                           availability=request.args["availability"],
                           amount=request.args["amount"],
                           price=request.args["price"])
        return 'New article added!', 201
    except sqlite3.IntegrityError as E:
        json["error"] = repr(E)
        return jsonify(json), 500


@app.route('/sql', methods=['DELETE'])
def sql_delete():
    json = {"error": None}
    try:
        db.delete_article(article_id=request.args["article_id"],)
        return jsonify(json), 200
    except Exception as E:
        json["error"] = repr(E)
        return jsonify(json), 500


if __name__ == '__main__':
    app.run()
