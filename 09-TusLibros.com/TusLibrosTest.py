import unittest
from TusLibros import ShoppingCart, Cashier, MerchantConnection, TransactionError, CreditCard, SalesBook
import math
from datetime import datetime


class MockMerchantConnection(MerchantConnection):
    def __init__(self, base_url):
        self.base_url = base_url

    def processTransaction(self, credit_card, transaction_amount):
        if credit_card.number == "5400000000000001" and \
                credit_card.owner == "PEPE SANCHEZ" and \
                math.fabs(transaction_amount - 123.5) < .1:
            return "TEST TRANSACTION ID"
        if credit_card.owner == "POOR PEPE":
            raise TransactionError("Credit card transaction without money")
        if credit_card.owner == "THIEF":
            raise TransactionError("Credit card stolen")
        raise TransactionError("Credit card transaction failed")


class ObjectFactory:
    def __init__(self):
        self.date_1yr_ahead = str(datetime.now().month).zfill(
            2) + str(datetime.now().year + 1)
        self.date_1yr_behind = str(datetime.now().month).zfill(
            2) + str(datetime.now().year - 1)

    def createCatalog(self):
        return {12345: 100, 111: 123.5}

    def createEmptyShoppingCart(self):
        return ShoppingCart(self.createCatalog())

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

    def createCashierWithMockMC(self, sales_book):
        return Cashier(
            self.createCatalog(), sales_book, MockMerchantConnection(
                "https://merchanttest.com/debit"))


class ShoppingCartTest(unittest.TestCase):

    def setUp(self):
        self.object_factory = ObjectFactory()
        self.cart = self.object_factory.createEmptyShoppingCart()

    def test01NewCartIsEmpty(self):
        self.assertEquals(self.cart.contents(), {})

    def test02AddingOneBookSucceedsWhenBookInCatalog(self):
        self.cart.add_book(12345, 4)
        self.assertEquals(self.cart.contents(), {12345: 4})

    def test03AddingOneBookFailsWhenBookNotInCatalog(self):
        try:
            self.cart.add_book(123456, 4)
            self.fail()
        except ValueError as e:
            self.assertEqual(e.message, "Book ISBN not in catalog")
            self.assertEquals(self.cart.contents(), {})

    def test04AddingMultipleDifferentBooksInCatalogSuceeds(self):
        self.cart.add_book(12345, 4)
        self.cart.add_book(111, 4)
        self.assertEquals(self.cart.contents(), {12345: 4, 111: 4})

    def test05AddingMultipleTimesSameBooksInCatalogSuceeds(self):
        self.cart.add_book(12345, 4)
        self.cart.add_book(12345, 3)
        self.assertEquals(self.cart.contents(), {12345: 7})

    def test06AddingNegativeQuantityFails(self):
        self.cart.add_book(12345, 4)
        try:
            self.cart.add_book(12345, -2)
            self.fail()
        except ValueError as e:
            self.assertEquals(
                e.message, "Book Quantity must be a positive integer")


class CreditCardTest(unittest.TestCase):
    def test01CannotCreateCCWithShorterNumber(self):
        try:
            cc = CreditCard("123456", "071993", "RENE FAVALORO")
            self.fail()
        except ValueError as e:
            self.assertEqual(e.message, "Credit card data has wrong format")

    def test02CannotCreateCCWithMonthBiggerThan12(self):
        try:
            cc = CreditCard("1234567890123456", "131993", "RENE FAVALORO")
            self.fail()
        except ValueError as e:
            self.assertEqual(e.message, "Credit card data has wrong format")

    def test03CannotCreateCCWithYearZero(self):
        try:
            cc = CreditCard("1234567890123456", "130000", "RENE FAVALORO")
            self.fail()
        except ValueError as e:
            self.assertEqual(e.message, "Credit card data has wrong format")

    def test04CannotCreateCCWithEmptyName(self):
        try:
            cc = CreditCard("1234567890123456", "130000", "")
            self.fail()
        except ValueError as e:
            self.assertEqual(e.message, "Credit card data has wrong format")

    def test04CannotCreateCCWithEmptyName(self):
        try:
            cc = CreditCard("1234567890123456", "130000", "")
            self.fail()
        except ValueError as e:
            self.assertEqual(e.message, "Credit card data has wrong format")

    def test05CanCreateCCWithCorrectData(self):
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
        self.client_id = "123ABC"

    def test01CashierWontCheckOutEmptyCart(self):
        try:
            transaction_id = self.cashier.check_out(
                self.client_id, self.cart, self.credit_card)
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
            transaction_id = self.cashier.check_out(self.client_id,
                                                    self.cart, new_credit_card_data)
            self.fail()
        except TransactionError as e:
            self.assertEqual(e.message, "Credit card expired")
            self.assertEqual(self.sales_book.get_purchases(
                self.client_id), ({}, 0.0))

    def test03CashiertWillCheckOutCartWithTestData(self):
        self.cart.add_book(111, 1)
        self.assertEqual("TEST TRANSACTION ID", self.cashier.check_out(self.client_id,
                                                                       self.cart, self.credit_card))
        self.assertEqual(self.sales_book.get_purchases(
            self.client_id), ({111: 1}, 123.5))

    def test04CashierWillFailWithoutMoneyInCreditCard(self):
        self.credit_card = self.object_factory.createBrokeCreditCard()
        self.cart.add_book(111, 1)

        try:
            transaction_id = self.cashier.check_out(
                self.client_id, self.cart, self.credit_card)
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
                self.client_id, self.cart, self.credit_card)
            self.fail()
        except TransactionError as e:
            self.assertEqual(e.message, "Credit card stolen")
            self.assertEqual(self.sales_book.get_purchases(
                self.client_id), ({}, 0.0))


if __name__ == "__main__":
    unittest.main()
