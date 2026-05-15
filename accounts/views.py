

# Create your views here.
from django.shortcuts import render , redirect
from django.http import JsonResponse
from django.views import View
from accounts.forms import BankAccountForm
from users.models import User
from accounts.models import BankAccount
from transactions.models import Transaction
from django.views.generic import ListView
import time
from django.utils.decorators import method_decorator
from accounts.services import AccountService

# Create your views here.

# def decorators(func):
#     def wrapper(*args, **kwargs):
#         start_time = time.time()
#         result = func(*args, **kwargs)
#         end_time = time.time()
#         print(f"Execution time: {end_time - start_time:.4f} seconds")
#         return result
#     return wrapper

# from datetime import datetime
# def log_file(func):
#     def wrapper(self, *args, **kwargs):
#         func(self ,*args, **kwargs)
#         time_log = datetime.now()
#         function_name = func.__name__
#         print(f"now running" , {function_name})
#         print(time_log)
#         user = self.account_no
#         balance = self.blnc
#         with open("log.csv" , "a") as f:
#             f.write(f"{time_log} , {function_name} , {user} , {balance} \n ")

#     return wrapper



# @method_decorator(decorators , name='dispatch')
# @method_decorator(log_file , name='dispatch')
class AccountApiView(View):
    def get(self, request, account_number):
      try:
            data = AccountService.get_account_data(
                account_number
            )

            return JsonResponse(data)

      except BankAccount.DoesNotExist:

            return JsonResponse(
                {'error': 'Account not found'},
                status=404
            )
        
# # @method_decorator(decorators)
# # @method_decorator(log_file)


class AccountListView(ListView):
    model = BankAccount
    template_name = 'account_list.html'
    context_object_name = 'accounts'
    
    # def get_queryset(self):
    #     return BankAccount.objects.order_by('-balance')

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = 'dashboard.html'


class createAccountView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = BankAccountForm()
        return render(request, 'create_account.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = BankAccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('dashboard')
        return render(request, 'create_account.html', {'form': form})


class withdrawView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'withdraw.html')
    def post(self, request, *args, **kwargs):
        account_number = request.POST.get('account_number')
        amount = float(request.POST.get('amount'))
        try:
            account = BankAccount.objects.get(account_number=account_number, user=request.user)
            if account.withdraw(amount):
                Transaction.objects.create(
                    account=account,
                    transaction_type='withdrawal',
                    amount=amount
                )
                return redirect('dashboard')
            else:
                return render(request, 'withdraw.html', {'error': 'Insufficient balance'})
        except BankAccount.DoesNotExist:
            return render(request, 'withdraw.html', {'error': 'Account not found'})
        
class depositView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'deposit.html')
    def post(self, request, *args, **kwargs):
        account_number = request.POST.get('account_number')
        amount = float(request.POST.get('amount'))
        try:
            account = BankAccount.objects.get(account_number=account_number, user=request.user)
            account.deposit(amount)
            Transaction.objects.create(
                account=account,
                transaction_type='deposit',
                amount=amount
            )
            return redirect('dashboard')
        except BankAccount.DoesNotExist:
            return render(request, 'deposit.html', {'error': 'Account not found'})
        
class transferView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        accounts = BankAccount.objects.filter(user=request.user)
        return render(request, 'transfer.html' , {'accounts': accounts})
    
    def post(self, request, *args, **kwargs):
        source_account_number = request.POST.get('source_account_number')
        target_account_number = request.POST.get('target_account_number')
        amount = float(request.POST.get('amount'))
        try:
            source_account = BankAccount.objects.get(account_number=source_account_number, user=request.user)
            target_account = BankAccount.objects.get(account_number=target_account_number)
            source_account.transfer(target_account, amount)
            Transaction.objects.create(
                account=source_account,
                transaction_type='transfer',
                amount=amount
            )
            return redirect('dashboard')
        except BankAccount.DoesNotExist:
            return render(request, 'transfer.html', {'error': 'Account not found'})
        except ValueError as e:
            return render(request, 'transfer.html', {'error': str(e)})
        
class functionalityView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'functions.html')