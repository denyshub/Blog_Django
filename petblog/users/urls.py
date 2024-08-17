from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .views import RegisterUser, ProfileUser

app_name = 'users'


urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('profile/', ProfileUser.as_view(), name='profile')
]

