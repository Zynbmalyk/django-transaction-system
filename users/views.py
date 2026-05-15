from django.shortcuts import render, redirect
from users.form import RegisterForm
from django.views import View

class registerView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'registration.html', {'form': form})
    

from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

class CustomLoginView(LoginView):
    template_name = 'login.html'

class CustomLogoutView(LogoutView):
    template_name = 'logout.html'
    next_page = 'login'
