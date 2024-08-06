from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse

menu = [{'title':'Головна', 'url': 'home' }, {'title':'Про сайт', 'url': 'about' }, { 'title':'Додати статтю', 'url': 'add_page'},{'title':'Зворотній зв\'язок', 'url':'contacts'},{'title':'Увійти', 'url':'login'}]

data_db = [
    {'id': 1, 'title': 'Новини дня', 'content': 'Свіжі новини', "is_published": True},
    {'id': 2, 'title': 'Ігри', 'content': 'Мої улюблені ігри', "is_published": False},
    {'id': 3, 'title': 'Прогулянка', 'content': 'Прогулянка містом', "is_published": True},

]

def index(request):
    data = {
        'title': 'Головна сторінка',
        'menu': menu,
        'posts': data_db
            }
    return render(request, 'blog/index.html', context = data)

def about(request):
    context = {'title': 'Про сайт', 'menu': menu}
    return render(request, 'blog/about.html', context)

def archive(request, year):
    if year > 2024:
        url = reverse('categories', args=('games',))
        return redirect(url)
    return HttpResponse(f'<h1>Архів {year} року</h1>')


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Сторінка не знайдена</h1>" )

def show_post(request, post_id):
    return HttpResponseNotFound(f"<h1>Пост з id: {post_id}</h1>")

def add_page(request):
    return HttpResponse("<h1>Додати пост</h1>")

def contacts(request):
    return HttpResponse("<h1>Контакти</h1>")

def login(request):
    return HttpResponse("<h1>Увійти</h1>")