import unittest
from TusLibros import *
import math
from datetime import datetime
from uuid import uuid4, UUID
from random import choice

class MockMerchantConnection(MerchantConnection):
    def __init__(self, base_url):
        self.base_url = base_url

    def processTransaction(self, credit_card, transaction_amount):
        if credit_card.number == "5400000000000001" and \
                credit_card.owner == "PEPE SANCHEZ":
            return "TEST TRANSACTION ID"
        if credit_card.owner == "POOR PEPE":
            raise TransactionError("Credit card transaction without money")
        if credit_card.owner == "THIEF":
            raise TransactionError("Credit card stolen")
        print(credit_card.number, credit_card.expiration_date, credit_card.owner)
        raise TransactionError("Credit card transaction failed")


class ObjectFactory:
    def __init__(self):
        self.date_1yr_ahead = str(datetime.now().month).zfill(
            2) + str(datetime.now().year + 1)
        self.date_1yr_behind = str(datetime.now().month).zfill(
            2) + str(datetime.now().year - 1)

    def createCatalog(self):
        return {12345: 100, 111: 123.5}

    def createBookIsbn(self):
        return 111

    def createOtherBookIsbn(self):
        return 12345

    def createClientId(self):
        return UUID('e9bbdaaf-b7b5-4d6a-b918-7dbf538a9603')

    def createEmptyShoppingCart(self):
        return ShoppingCart(self.createClientId(), self.createCatalog())

    def createGoodCreditCard(self):
        return CreditCard("5400000000000001", self.date_1yr_ahead, "PEPE SANCHEZ")

    def createExpiredCreditCard(self):
        return CreditCard("5400000000000001", self.date_1yr_behind, "PEPE SANCHEZ")

    def createBrokeCreditCard(self):
        return CreditCard("5400000000000001", self.date_1yr_ahead, "POOR PEPE")

    def createStolenCreditCard(self):
        return CreditCard("5400000000000001", self.date_1yr_ahead, "THIEF")

    def createEmptySalesBook(self):
        return SalesBook()

    def createMockMC(self):
        return MockMerchantConnection("https://merchanttest.com/debit")

    def createCashierWithMockMC(self, sales_book):
        return Cashier(sales_book, self.createMockMC())


class ShoppingCartTest(unittest.TestCase):

    def setUp(self):
        self.object_factory = ObjectFactory()
        self.cart = self.object_factory.createEmptyShoppingCart()

    def test01NewCartIsEmpty(self):
        self.assertEqual(self.cart.contents(), {})

    def test02AddingOneBookSucceedsWhenBookInCatalog(self):
        self.cart.add_book(12345, 4)
        self.assertEqual(self.cart.contents(), {12345: 4})

    def test03AddingOneBookFailsWhenBookNotInCatalog(self):
        try:
            self.cart.add_book(123456, 4)
            self.fail()
        except ValueError as e:
            self.assertEqual(e.message, "Book ISBN not in catalog")
            self.assertEqual(self.cart.contents(), {})

    def test04AddingMultipleDifferentBooksInCatalogSuceeds(self):
        self.cart.add_book(12345, 4)
        self.cart.add_book(111, 4)
        self.assertEqual(self.cart.contents(), {12345: 4, 111: 4})

    def test05AddingMultipleTimesSameBooksInCatalogSuceeds(self):
        self.cart.add_book(12345, 4)
        self.cart.add_book(12345, 3)
        self.assertEqual(self.cart.contents(), {12345: 7})

    def test06AddingNegativeQuantityFails(self):
        self.cart.add_book(12345, 4)
        try:
            self.cart.add_book(12345, -2)
            self.fail()
        except ValueError as e:
            self.assertEqual(
                e.message, "Book Quantity must be a positive integer")


class CreditCardTest(unittest.TestCase):

    def test01CannotCreateCCWithEmptyName(self):
        try:
            cc = CreditCard("1234567890123456", "131993", "")
            self.fail()
        except ValueError as e:
            self.assertEqual(e.message, "Credit card data has wrong format")

    def test02CannotCreateCCWithEmptyExpiratationDate(self):
        try:
            cc = CreditCard("1234567890123456", "", "RENE FAVALORO")
            self.fail()
        except ValueError as e:
            self.assertEqual(e.message, "Credit card data has wrong format")
    
    def test03CannotCreateCCWithEmptyCreditCardNumber(self):
        try:
            cc = CreditCard("", "131993", "RENE FAVALORO")
            self.fail()
        except ValueError as e:
            self.assertEqual(e.message, "Credit card data has wrong format")


    def test04CannotCreateCCWithShorterNumber(self):
        try:
            cc = CreditCard("123456", "071993", "RENE FAVALORO")
            self.fail()
        except ValueError as e:
            self.assertEqual(e.message, "Credit card data has wrong format")

    def test05CannotCreateCCWithMonthBiggerThan12(self):
        try:
            cc = CreditCard("1234567890123456", "131993", "RENE FAVALORO")
            self.fail()
        except ValueError as e:
            self.assertEqual(e.message, "Credit card data has wrong format")

    def test06CannotCreateCCWithYearZero(self):
        try:
            cc = CreditCard("1234567890123456", "130000", "RENE FAVALORO")
            self.fail()
        except ValueError as e:
            self.assertEqual(e.message, "Credit card data has wrong format")

    def test07CanCreateCCWithCorrectData(self):
        cc = CreditCard("1234567890123456", "022012", "RENE FAVALORO")
        self.assertEqual(cc.number, "1234567890123456")
        self.assertEqual(cc.expiration_date.year, 2012)
        self.assertEqual(cc.expiration_date.month, 2)
        self.assertEqual(cc.expiration_date.day, 29)
        self.assertEqual(cc.owner, "RENE FAVALORO")


class CashierTest(unittest.TestCase):

    def setUp(self):
        self.object_factory = ObjectFactory()
        self.cart = self.object_factory.createEmptyShoppingCart()
        self.credit_card = self.object_factory.createGoodCreditCard()
        self.sales_book = self.object_factory.createEmptySalesBook()
        self.cashier = self.object_factory.createCashierWithMockMC(
            self.sales_book)
        self.client_id = uuid4()

    def test01CashierWontCheckOutEmptyCart(self):
        try:
            transaction_id = self.cashier.check_out(
                self.cart, self.credit_card)
            self.fail()
        except ValueError as e:
            self.assertEqual(e.message, "Cannot check out empty cart")
            self.assertEqual(self.sales_book.get_purchases(
                self.client_id), ({}, 0.0))

    def test02CashierWontCheckOutExpiredCreditCard(self):
        self.cart.add_book(111, 1)
        now = datetime.now()

        new_credit_card_data = self.object_factory.createExpiredCreditCard()
        try:
            transaction_id = self.cashier.check_out(
                self.cart, new_credit_card_data)
            self.fail()
        except TransactionError as e:
            self.assertEqual(e.message, "Credit card expired")
            self.assertEqual(self.sales_book.get_purchases(
                self.client_id), ({}, 0.0))

    def test03CashiertWillCheckOutCartWithTestData(self):
        self.cart.add_book(111, 1)
        self.assertEqual("TEST TRANSACTION ID",
                         self.cashier.check_out(self.cart, self.credit_card))
        self.assertEqual(self.sales_book.get_purchases(
            self.cart.client_id()), ({111: 1}, 123.5))

    def test04CashierWillFailWithoutMoneyInCreditCard(self):
        self.credit_card = self.object_factory.createBrokeCreditCard()
        self.cart.add_book(111, 1)

        try:
            transaction_id = self.cashier.check_out(
                self.cart, self.credit_card)
            self.fail()
        except TransactionError as e:
            self.assertEqual(
                e.message, "Credit card transaction without money")
            self.assertEqual(self.sales_book.get_purchases(
                self.client_id), ({}, 0.0))

    def test05CashierWillFailStolenCreditCard(self):
        self.credit_card = self.object_factory.createStolenCreditCard()
        self.cart.add_book(111, 1)

        try:
            transaction_id = self.cashier.check_out(
                self.cart, self.credit_card)
            self.fail()
        except TransactionError as e:
            self.assertEqual(e.message, "Credit card stolen")
            self.assertEqual(self.sales_book.get_purchases(
                self.client_id), ({}, 0.0))


class WebInterfaceTest(unittest.TestCase):
    def setUp(self):
        self.object_factory = ObjectFactory()
        self.catalog = self.object_factory.createCatalog()
        self.empty_interface = WebInterface(
            {}, self.catalog, self.object_factory.createMockMC(), 30)
        self.user_id = uuid4()
        self.password = 'hello1234'
        self.interface = WebInterface(
            {self.user_id: self.password}, self.catalog, self.object_factory.createMockMC(), 30)
        self.die_fast_interface = WebInterface(
            {self.user_id: self.password}, self.catalog, self.object_factory.createMockMC(), 0)

    def test01WontCreateCartWithNonExistentUser(self):
        try:
            self.empty_interface.create_cart(self.user_id, self.password)
            self.fail()
        except AuthenticationError as e:
            self.assertEqual(e.message, "User not known")

    def test02WontCreateCartWithWrongPassword(self):
        try:
            self.interface.create_cart(self.user_id, 'goodbye9876')
            self.fail()
        except AuthenticationError as e:
            self.assertEqual(e.message, "Wrong password")

    def test03CreatesEmptyCartWithCorrectCredentials(self):
        cart_id = self.interface.create_cart(self.user_id, self.password)
        self.assertEqual(self.interface.list_cart(cart_id), {})

    def test04WontListNonExistantCart(self):
        cart_id = uuid4()
        try:
            contents = self.interface.list_cart(cart_id)
            self.fail()
        except KeyError as e:
            self.assertEqual(e.message, "Shopping cart not known")

    def test05AddsBookToCart(self):
        cart_id = self.interface.create_cart(self.user_id, self.password)
        quantity = 7
        self.assertTrue(self.interface.add_to_cart(
            cart_id, self.object_factory.createBookIsbn(), quantity))
        self.assertEqual(self.interface.list_cart(cart_id), {
                         self.object_factory.createBookIsbn(): quantity})

    def test06AddToCartFailsAfterCartTimesOut(self):

        cart_id = self.die_fast_interface.create_cart(self.user_id, self.password)
        try:
            self.die_fast_interface.add_to_cart(
                cart_id, self.object_factory.createBookIsbn(), 3)
            self.fail()
        except TimeoutError as e:
            self.assertEqual(e.message, "Shopping cart has expired")

    def test07ChecksOutCart(self):
        cart_id = self.interface.create_cart(self.user_id, self.password)
        cc = self.object_factory.createGoodCreditCard()
        quantity = 1
        self.interface.add_to_cart(
            cart_id, self.object_factory.createBookIsbn(), quantity)

        exp_date = str(cc.expiration_date.month).zfill(
            2) + str(cc.expiration_date.year)
        transaction_id = self.interface.check_out_cart(
            cart_id, cc.number, exp_date, cc.owner)
        self.assertEqual(transaction_id, "TEST TRANSACTION ID")
        self.assertEqual(self.interface.list_purchases(
            self.user_id), ({111: 1}, 123.5))

    def test09ListsAllPurchases(self):
        cart1_id = self.interface.create_cart(self.user_id, self.password)
        cart2_id = self.interface.create_cart(self.user_id, self.password)
        cart3_id = self.interface.create_cart(self.user_id, self.password)
        cc = self.object_factory.createGoodCreditCard()

        self.interface.add_to_cart(
            cart1_id, self.object_factory.createBookIsbn(), 3)
        self.interface.add_to_cart(
            cart2_id, self.object_factory.createBookIsbn(), 4)
        self.interface.add_to_cart(
            cart3_id, self.object_factory.createOtherBookIsbn(), 3)

        exp_date = str(cc.expiration_date.month).zfill(
            2) + str(cc.expiration_date.year)
        self.interface.check_out_cart(cart1_id, cc.number, exp_date, cc.owner)
        self.interface.check_out_cart(cart2_id, cc.number, exp_date, cc.owner)
        self.interface.check_out_cart(cart3_id, cc.number, exp_date, cc.owner)
        print self.interface.list_purchases(self.user_id)
        self.assertEqual(self.interface.list_purchases(
            self.user_id), ({111: 7, 12345: 3}, 123.5 * 7 + 100 * 3))




if __name__ == "__main__":
    unittest.main()
