
from collections import Counter
import datetime
import re
import calendar
from uuid import uuid4

class WebInterface:
    def __init__(self, userbase, catalog, merchant_processor, cart_timeout):
        self.__userbase = userbase
        self.__catalog = catalog
        self.__merchant_processor = merchant_processor
        self.__cart_timeout = datetime.timedelta(minutes=cart_timeout)
        self.__carts = {}
        self.__cart_timestamps = {}
        self.__sales_book = SalesBook()

    def __verify_timeout(self, cart_id):
        if datetime.datetime.now() - self.__cart_timestamps[cart_id] > self.__cart_timeout:
            raise TimeoutError("Shopping cart has expired")
    
    def __update_timestamp(self, cart_id):
        self.__cart_timestamps[cart_id] = datetime.datetime.now()

    def create_cart(self, client_id, password):
        if client_id in self.__userbase:
            if self.__userbase[client_id] == password:
                cart_id = uuid4()
                self.__carts[cart_id] = ShoppingCart(client_id, self.__catalog)
                self.__update_timestamp(cart_id)
                return cart_id
            else:
                raise AuthenticationError("Wrong password")
        else:
            raise AuthenticationError("User not known")

    def list_cart(self, cart_id):
        try:
            self.__verify_timeout(cart_id)
            self.__update_timestamp(cart_id)
            return self.__carts[cart_id].contents()
        except KeyError:
            raise KeyError("Shopping cart not known")

    def add_to_cart(self, cart_id, isbn, quantity):
        try:
            self.__verify_timeout(cart_id)
            self.__update_timestamp(cart_id)
            return self.__carts[cart_id].add_book(isbn, quantity)
        except KeyError:
            raise KeyError("Shopping cart not known")

    def check_out_cart(self, cart_id, ccn, cced, cco):
        cashier = Cashier(self.__sales_book, self.__merchant_processor)
        try:
            self.__verify_timeout(cart_id)
            self.__update_timestamp(cart_id)
            return cashier.check_out(self.__carts[cart_id], CreditCard(ccn, cced, cco))
        except KeyError:
            raise KeyError("Shopping cart not known")

    def list_purchases(self, client_id):
        if client_id in self.__userbase:
            return self.__sales_book.get_purchases(client_id)
        else:
            raise AuthenticationError("User not known")
        


class ShoppingCart:
    def __init__(self, client_id, catalog):
        self.__client_id = client_id
        self.__catalog = catalog
        self.__books = Counter()

    def add_book(self, book_isbn, book_quantity):
        if book_isbn not in self.__catalog:
            raise ValueError("Book ISBN not in catalog")
        if book_quantity <= 0:
            raise ValueError("Book Quantity must be a positive integer")
        self.__books[book_isbn] += int(book_quantity)
        return True

    def contents(self):
        return self.__books

    def total_price(self):
        amount = 0.0
        for book in self.__books:
            amount += self.__books[book] * self.__catalog[book]
        return amount

    def client_id(self):
        return self.__client_id


class SalesBook:
    def __init__(self):
        self.__book = {}
        self.__sale_amounts = Counter()

    def add_sale(self, cart):
        if cart.client_id() not in self.__book:
            self.__book[cart.client_id()] = Counter()
        self.__book[cart.client_id()] += cart.contents()
        self.__sale_amounts[cart.client_id()] += cart.total_price()

    def get_purchases(self, client_id):
        if client_id in self.__book:
            return (self.__book[client_id], self.__sale_amounts[client_id])
        else:
            return (Counter(), 0.0)


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
    def __init__(self, sales_book, merchant_connection):
        self.__sales_book = sales_book
        self.__merchant_connection = merchant_connection

    def check_out(self, cart, credit_card):
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

        self.__sales_book.add_sale(cart)

        return transaction_id


class TransactionError(Exception):
    def __init__(self, message):
        self.message = message

class AuthenticationError(Exception):
    def __init__(self, message):
        self.message = message

class TimeoutError(Exception):
    def __init__(self, message):
        self.message = message


class MerchantConnection:
    def __init__(self, url):
        pass
