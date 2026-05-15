from django.urls import path 
from users.views import registerView , CustomLoginView , CustomLogoutView

urlpatterns = [
    path('register/', registerView.as_view(), name='register'),
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]