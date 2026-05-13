from django.core.management.base import BaseCommand
from bank.models import BankAccount, Transaction
from django.utils.decorators import method_decorator
import json
from datetime import datetime 
import time
from functools import wraps


# def func():
#     fun = BankAccount.__name__
#     return fun

def transaction_generator(transaction):
    for t in transaction:
        yield t

def decorators(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time} seconds")
        return result
    return wrapper

def log_file(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        func(self ,*args, **kwargs)
        time_log = datetime.now()
        function_name = func.__qualname__.split('.')[0]
        print(f"now running" , {function_name})
        print(time_log)
        user = BankAccount.account_number
        balance = BankAccount.balance
        with open("log.csv" , "a") as f:
            f.write(f"{time_log} , {function_name} , {user} , {balance} \n ")

    return wrapper



# @method_decorator(decorators , name='decorator')
# @method_decorator(log_file , name='log_file')
class Command(BaseCommand):
    #    def handle(self, *args, **kwargs):
    #        print("Processing transactions...")
    # success = 0
    # failed = 0

    def add_arguments(self, parser):
            parser.add_argument('file_path', type=str)

  

    @log_file
    @decorators
    def handle(self, *args, **kwargs):
            success = 0
            failed = 0
            file_path = kwargs['file_path']
            with open(file_path, 'r') as file:
                transactions_data = json.load(file)

            for transaction_data in transactions_data:
                try:
                    source_account = BankAccount.objects.get(account_number=transaction_data['source_account'])
                    target_account = BankAccount.objects.get(account_number=transaction_data['target_account'])
                    amount = transaction_data['amount']
                    transaction_type = transaction_data['transaction_type']

                    if transaction_type == 'DEPOSIT':
                        source_account.deposit(amount)
                        Transaction.objects.create(
                            transaction_type='DEPOSIT',
                            amount=amount,
                            source_account=source_account,
                            target_account=target_account,
                            status='COMPLETED'
                        )
                        success += 1
                    elif transaction_type == 'WITHDRAWAL':
                        if source_account.withdraw(amount):
                            Transaction.objects.create(
                                transaction_type='WITHDRAWAL',
                                amount=amount,
                                source_account=source_account,
                                target_account=target_account,
                                status='COMPLETED'
                            )
                            success += 1
                        else:
                            Transaction.objects.create(
                                transaction_type='WITHDRAWAL',
                                amount=amount,
                                source_account=source_account,
                                target_account=target_account,
                                status='FAILED',
                                message='Insufficient balance'
                            )
                            failed += 1
                    elif transaction_type == 'TRANSFER':
                        try:
                            source_account.transfer(target_account, amount)
                            Transaction.objects.create(
                                transaction_type='TRANSFER',
                                amount=amount,
                                source_account=source_account,
                                target_account=target_account,
                                status='COMPLETED'
                            )
                            success += 1
                        except ValueError as e:
                            Transaction.objects.create(
                                transaction_type='TRANSFER',
                                amount=amount,
                                source_account=source_account,
                                target_account=target_account,
                                status='FAILED',
                                message=str(e)
                            )
                            failed += 1
                except BankAccount.DoesNotExist:
                    print(f"Account not found for transaction: {transaction_data}")

            self.stdout.write(f"Processing completed. Successful: {success}, Failed: {failed}")


            accounts = BankAccount.objects.all()
            for account in accounts:
                print(f"Account: {account.account_number}, Balance: {account.balance}")

            highest_balance_account = BankAccount.objects.order_by('-balance').first()
            if highest_balance_account:
                print(f"Account with highest balance: {highest_balance_account.account_number}, Balance: {highest_balance_account.balance}")


            total_balance = sum(account.balance for account in accounts)
            print(f"Total balance across all accounts: {total_balance}")


            for transaction in transaction_generator(Transaction.objects.all()):
                # yield transaction
                print(f"Transaction: {transaction.transaction_type}, Amount: {transaction.amount}, Status: {transaction.status}")