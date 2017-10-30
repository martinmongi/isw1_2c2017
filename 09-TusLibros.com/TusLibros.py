
from collections import Counter
import datetime
import re
import calendar


class ShoppingCart:
    def __init__(self, catalog):
        self.__catalog = catalog
        self.__books = Counter()

    def addBook(self, bookIsbn, bookQuantity):
        if bookIsbn not in self.__catalog:
            raise ValueError("Book ISBN not in catalog")
        if bookQuantity <= 0:
            raise ValueError("Book Quantity must be a positive integer")
        self.__books[bookIsbn] += int(bookQuantity)

    def contents(self):
        return self.__books


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
    def __init__(self, catalog, merchant_connection):
        self.__catalog = catalog
        self.__merchant_connection = merchant_connection

    def checkOut(self, cart, credit_card):
        if not cart.contents():
            raise ValueError("Cannot check out empty cart")

        now = datetime.datetime.now()
        if now.year > credit_card.expiration_date.year or \
                now.year == credit_card.expiration_date.year and \
                now.month < credit_card.expiration_date.month:
            raise TransactionError("Credit card expired")

        amount = 0.0
        for book in cart.contents():
            amount += cart.contents()[book] * self.__catalog[book]
        return self.__merchant_connection.processTransaction(credit_card, amount)


class TransactionError(Exception):
    def __init__(self, message):
        self.message = message


class MerchantConnection:
    def __init__(self, url):
        pass
