import unittest
from TusLibros import ShoppingCart, Cashier, MerchantConnection, TransactionError
import math


class MockMerchantConnection(MerchantConnection):
    def __init__(self, base_url):
        self.base_url = base_url

    def processTransaction(self, creditCardData, transactionAmount):
        if creditCardData == ("5400000000000001", "072011", "PEPE SANCHEZ") and \
                math.fabs(transactionAmount - 123.5) < .1:
            return "TEST TRANSACTION ID"
        raise TransactionError("Credit card transaction failed")


class ShoppingCartTest(unittest.TestCase):

    def setUp(self):
        self.catalog = {12345: 100, 111: 123.5}
        self.cart = ShoppingCart(self.catalog)

    def test01NewCartIsEmpty(self):
        self.assertEquals(self.cart.contents(), {})

    def test02AddingOneBookSucceedsWhenBookInCatalog(self):
        self.cart.addBook(12345, 4)
        self.assertEquals(self.cart.contents(), {12345: 4})

    def test03AddingOneBookFailsWhenBookNotInCatalog(self):
        try:
            self.cart.addBook(123456, 4)
            self.fail()
        except ValueError as e:
            self.assertEqual(e.message, "Book ISBN not in catalog")
            self.assertEquals(self.cart.contents(), {})

    def test04AddingMultipleDifferentBooksInCatalogSuceeds(self):
        self.cart.addBook(12345, 4)
        self.cart.addBook(111, 4)
        self.assertEquals(self.cart.contents(), {12345: 4, 111: 4})

    def test05AddingMultipleTimesSameBooksInCatalogSuceeds(self):
        self.cart.addBook(12345, 4)
        self.cart.addBook(12345, 3)
        self.assertEquals(self.cart.contents(), {12345: 7})

    def test06AddingNegativeQuantityFails(self):
        self.cart.addBook(12345, 4)
        try:
            self.cart.addBook(12345, -2)
            self.fail()
        except ValueError as e:
            self.assertEquals(
                e.message, "Book Quantity must be a positive integer")


class CashierTest(unittest.TestCase):

    def setUp(self):
        self.catalog = {12345: 100, 111: 123.5}
        self.cart = ShoppingCart(self.catalog)
        self.merchant_connection = MockMerchantConnection(
            "https://merchanttest.com/debit")
        self.credit_card_data = ("5400000000000001", "072011", "PEPE SANCHEZ")
        self.cashier = Cashier(self.catalog, self.merchant_connection)

    def test01CashierWontCheckOutEmptyCart(self):
        try:
            transaction_id = self.cashier.checkOut(
                self.cart, self.credit_card_data)
            self.fail()
        except ValueError as e:
            self.assertEqual(e.message, "Cannot check out empty cart")

    def test02CashiertWillCheckOutCartWithTestData(self):
        self.cart.addBook(111, 1)
        self.assertEqual("TEST TRANSACTION ID", self.cashier.checkOut(
            self.cart, self.credit_card_data))

    def test03CashierWillFailWithWrongData(self):
        self.cart.addBook(111, 2)
        try:
            transaction_id = self.cashier.checkOut(
                self.cart, self.credit_card_data)
            self.fail()
        except TransactionError as e:
            self.assertEqual(e.message, "Credit card transaction failed")


if __name__ == "__main__":
    unittest.main()
