from django.db import models
from accounts.models import BankAccount


# Create your models here.
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
        return f"{self.transaction_type} of {self.amount} from {self.source_account.user.first_name} to {self.target_account.user.first_name} - {self.status}"
    

