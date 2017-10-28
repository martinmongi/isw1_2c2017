
from collections import Counter


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


class Cashier:
    def __init__(self, catalog, merchant_connection):
        self.__catalog = catalog
        self.__merchant_connection = merchant_connection

    def checkOut(self, cart, credit_card_data):
        if not cart.contents():
            raise ValueError("Cannot check out empty cart")
        amount = 0.0
        for book in cart.contents():
            amount += cart.contents()[book] * self.__catalog[book]
        return self.__merchant_connection.processTransaction(credit_card_data, amount)


class TransactionError(Exception):
    def __init__(self, message):
        self.message = message


class MerchantConnection:
    def __init__(self, url):
        pass
