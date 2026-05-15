from django.contrib import admin

from accounts.models import BankAccount

# Register your models here.
@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'balance', 'is_active')
    search_fields = ('account_number', )