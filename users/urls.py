from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('auth/', views.login_register_view, name='login_register'),
    path('profile/', views.profile_view, name='profile'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('logout/', views.logout_view, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
]
