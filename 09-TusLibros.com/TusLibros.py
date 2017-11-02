
from collections import Counter
import datetime
import re
import calendar


class ShoppingCart:
    def __init__(self, catalog):
        self.__catalog = catalog
        self.__books = Counter()

    def add_book(self, book_isbn, book_quantity):
        if book_isbn not in self.__catalog:
            raise ValueError("Book ISBN not in catalog")
        if book_quantity <= 0:
            raise ValueError("Book Quantity must be a positive integer")
        self.__books[book_isbn] += int(book_quantity)

    def contents(self):
        return self.__books

    def total_price(self):
        amount = 0.0
        for book in self.__books:
            amount += self.__books[book] * self.__catalog[book]
        return amount


class SalesBook:
    def __init__(self):
        self.__book = {}
        self.__sale_amounts = Counter()

    def add_sale(self, client_id, cart):
        if client_id not in self.__book:
            self.__book[client_id] = Counter()
        self.__book[client_id] += cart.contents()
        self.__sale_amounts[client_id] += cart.total_price()


class CreditCard:
    def __init__(self, number, expiration_date, owner):
        if not re.match("^[0-9]{16}$", number) or \
                not re.match("^[0-9]{6}$", expiration_date) or \
                not re.match("^([A-Z]+\s)*[A-Z]", owner) or \
                len(owner) > 30:
            raise ValueError("Credit card data has wrong format")
        self.number = number
        try:
            self.expiration_date = datetime.date(int(expiration_date[2:]), int(
                expiration_date[:2]), calendar.monthrange(int(expiration_date[2:]), int(expiration_date[:2]))[1])
        except calendar.IllegalMonthError as e:
            raise ValueError("Credit card data has wrong format")
        except ValueError as e:
            raise ValueError("Credit card data has wrong format")
        self.owner = owner


class Cashier:
    def __init__(self, catalog, sales_book, merchant_connection):
        self.__catalog = catalog
        self.__sales_book = sales_book
        self.__merchant_connection = merchant_connection

    def check_out(self, client_id, cart, credit_card):
        if not cart.contents():
            raise ValueError("Cannot check out empty cart")

        now = datetime.datetime.now()
        if now.year > credit_card.expiration_date.year or \
                now.year == credit_card.expiration_date.year and \
                now.month < credit_card.expiration_date.month:
            raise TransactionError("Credit card expired")

        amount = cart.total_price()
        transaction_id = self.__merchant_connection.processTransaction(
            credit_card, amount)

        self.__sales_book.add_sale(client_id, cart)

        return transaction_id


class TransactionError(Exception):
    def __init__(self, message):
        self.message = message


class MerchantConnection:
    def __init__(self, url):
        pass
