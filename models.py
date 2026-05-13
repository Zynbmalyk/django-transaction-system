from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    user_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

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
        
    

class Transaction(models.Model):
    transacion_choices = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('TRANSFER', 'Transfer'),
    ]
    status_choices = [
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

 
    transaction_type = models.CharField(max_length=10 , choices=transacion_choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source_account = models.ForeignKey(BankAccount, related_name='source_transactions', on_delete=models.CASCADE)
    target_account = models.ForeignKey(BankAccount, related_name='target_transactions', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=status_choices, default='PENDING')
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} from {self.source_account.user.name} to {self.target_account.user.name} - {self.status}"