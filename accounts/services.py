from accounts.models import BankAccount


class AccountService:

    @staticmethod
    def get_account_data(account_number):

        account = BankAccount.objects.get(
            account_number=account_number
        )

        return {
            'user': account.user.name,
            'account_number': account.account_number,
            'balance': str(account.balance),
            'is_active': account.is_active
        }