from django.test import TestCase
from bank.models import User, BankAccount, Transaction
# Create your tests here.
class BankAccountTestCase(TestCase):
    def setUp(self):

           self.user = User.objects.create(
        name="Ali",
        email="ali@gmail.com",
        user_code="U001"
    )

           self.account = BankAccount.objects.create(
        user=self.user,
        account_number="ACC1001",
        balance=1000
    )
    def test_deposit(self):
        self.account.deposit(500)
        self.assertEqual(self.account.balance, 1500)
    def test_withdraw(self):
        result = self.account.withdraw(300)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 700)
    def test_transfer(self):
        target_user = User.objects.create(
            name="Sara",
            email="sara@gmail.com",
            user_code="U002"
        )
        target_account = BankAccount.objects.create(
            user=target_user,
            account_number="ACC1002",
            balance=500
        )
        result = self.account.transfer(target_account, 300)
        # self.assertTrue(result)
        self.account.refresh_from_db()
        target_account.refresh_from_db()
        self.assertEqual(self.account.balance, 700)
        self.assertEqual(target_account.balance, 800)
