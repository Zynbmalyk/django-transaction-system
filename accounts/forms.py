from django import forms
from accounts.models import BankAccount

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['account_number', 'balance', 'is_active']