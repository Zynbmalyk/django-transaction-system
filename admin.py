from django.contrib import admin
from bank.models import User, BankAccount, Transaction
# Register your models here.

# class customization(admin.ModelAdmin):
#     list_filter = ('status' , )
#     search_fields = ('account_number' ,)


# admin.site.register(User , customization)
# admin.site.register(BankAccount , customization)
# admin.site.register(Transaction, customization)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'user_code')
    search_fields = ('name', 'email', 'user_code')

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_number', 'balance', 'is_active')
    search_fields = ('account_number', )

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'amount', 'source_account', 'target_account', 'status', 'created_at')
    list_filter = ('transaction_type', 'status')
    search_fields = ('source_account__account_number', )