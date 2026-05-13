from django.contrib import admin

from transactions.models import Transaction

# Register your models here.
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'amount', 'source_account', 'target_account', 'status', 'created_at')
    list_filter = ('transaction_type', 'status')
    search_fields = ('source_account__account_number', 'target_account__account_number')