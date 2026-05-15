
from django.test import TestCase
from accounts.models import BankAccount
from users.models import User
# Create your tests here.

class BankAccountTestCase(TestCase):
    def setUp(self):

        self.user = User.objects.create(
            name="Ali",
            email="ali@gmail.com",
            user_code="USR001"
        )

        self.account1 = BankAccount.objects.create(
            user=self.user, 
            account_number="ACC1001",
            balance=1000,
            is_active=True
        )
        self.account2 = BankAccount.objects.create(
            user=self.user, 
            account_number="ACC1002",
            balance=500,
            is_active=True
        )

    def test_deposit(self):
        self.account1.deposit(200)
        self.assertEqual(self.account1.balance, 1200)

    def test_withdraw(self):
        result = self.account1.withdraw(300)
        self.assertTrue(result)
        self.assertEqual(self.account1.balance, 700)


    def test_transfer(self):
        self.account1.transfer(self.account2, 400)

        self.account1.refresh_from_db()
        self.account2.refresh_from_db()

        self.assertEqual(self.account1.balance, 600)
        self.assertEqual(self.account2.balance, 900)



