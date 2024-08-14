from django.urls import path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.BlogHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('add_post/', views.AddPage.as_view(), name='add_post'),
    path('contacts/', views.contacts, name='contacts'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('archive/<year4:year>/', views.archive, name='archive'),
    path('category/<slug:category_slug>/', views.PostCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.PostTags.as_view(), name = 'tag')
]

