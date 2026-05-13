from django.db import transaction

from accounts.models import BankAccount
from transactions.models import Transaction


class TransactionService:

    @staticmethod
    @transaction.atomic
    def deposit(source_account, target_account, amount):

        source_account.deposit(amount)

        Transaction.objects.create(
            transaction_type='DEPOSIT',
            amount=amount,
            source_account=source_account,
            target_account=target_account,
            status='COMPLETED'
        )

    @staticmethod
    @transaction.atomic
    def withdraw(source_account, target_account, amount):

        if source_account.withdraw(amount):

            Transaction.objects.create(
                transaction_type='WITHDRAWAL',
                amount=amount,
                source_account=source_account,
                target_account=target_account,
                status='COMPLETED'
            )

            return True

        Transaction.objects.create(
            transaction_type='WITHDRAWAL',
            amount=amount,
            source_account=source_account,
            target_account=target_account,
            status='FAILED',
            message='Insufficient balance'
        )

        return False
    
    @staticmethod
    @transaction.atomic
    def transfer(source_account, target_account, amount):

        try:

            source_account.transfer(
                target_account,
                amount
            )

            Transaction.objects.create(
                transaction_type='TRANSFER',
                amount=amount,
                source_account=source_account,
                target_account=target_account,
                status='COMPLETED'
            )

            return True

        except ValueError as e:

            Transaction.objects.create(
                transaction_type='TRANSFER',
                amount=amount,
                source_account=source_account,
                target_account=target_account,
                status='FAILED',
                message=str(e)
            )

            return False