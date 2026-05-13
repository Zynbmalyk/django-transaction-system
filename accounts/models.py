from django.db import models
from users.models import User

# Create your models here.
class BankAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2 , default=0.00)
    is_active = models.BooleanField(default=True)

    def deposit(self, amount):
        if not self.is_active:
            raise ValueError("Account is not active.")
        self.balance += amount
        self.save()

    def withdraw(self,amount):
        if not self.is_active:
            raise ValueError("Account is not active.")
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False
    def transfer(self, target_account, amount):
        if not self.is_active:
            raise ValueError("Account is not active.")
        if not target_account.is_active:
            raise ValueError("Target account is not active.")
        if self == target_account:
            raise ValueError("Cannot transfer to the same account.")
        if self.balance < amount:
            raise ValueError("Insufficient balance.")
        
        self.balance -= amount
        target_account.balance += amount

        self.save()
        target_account.save()

    def __str__(self):
        return f"{self.user.name} - {self.account_number}"