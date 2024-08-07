from django.urls import path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('add_page/', views.add_page, name='add_page'),
    path('contacts/', views.contacts, name='contacts'),
    path('login/', views.login, name='login'),
    path('post/<int:post_id>/', views.show_post, name='post'),
    path('archive/<year4:year>/', views.archive, name='archive'),
    path('category/<int:category_id>/', views.show_category, name='category')
]

