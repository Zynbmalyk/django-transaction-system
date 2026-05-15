from django.urls import path

from accounts.views import DashboardView, createAccountView , withdrawView , depositView , transferView , functionalityView


urlpatterns = [

    path('dashboard/', DashboardView.as_view(),  name='dashboard' ),
    path('create-account/', createAccountView.as_view(), name='create_account'),
    path('withdraw/', withdrawView.as_view(), name='withdraw'),
    path('deposit/', depositView.as_view(), name='deposit'),    
    path('transfer/', transferView.as_view(), name='transfer'),
    path('functions/', functionalityView.as_view(), name='functions'),
]
