from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
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

