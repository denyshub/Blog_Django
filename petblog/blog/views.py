from django.db.models import Count
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from blog.models import Post, Category, TagPost

menu = [{'title':'Головна', 'url': 'home' }, {'title':'Про сайт', 'url': 'about' }, { 'title':'Додати статтю', 'url': 'add_page'},{'title':'Зворотній зв\'язок', 'url':'contacts'}]

def index(request):
    posts = Post.published.all().select_related('category')
    data = {
        'title': 'Головна сторінка',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
        'menu_selected': 'home',
                         'tag_selected':0
            }
    return render(request, 'blog/index.html', context = data)

def about(request):
    data = {
        'title': 'Про сайт',
        'menu': menu,
        'menu_selected': 'about'
    }
    return render(request, 'blog/about.html', context = data)

def archive(request, year):
    if year > 2024:
        url = reverse('categories', args=('games',))
        return redirect(url)
    return HttpResponse(f'<h1>Архів {year} року</h1>')


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Сторінка не знайдена</h1>" )

def show_post(request, post_slug):
    post = get_object_or_404(Post, slug = post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1
    }

    return render(request, 'blog/post.html', context=data)

def add_page(request):
    data = {
        'title': 'Додати пост',
        'menu': menu,
        'menu_selected': 'add_post'
    }
    return HttpResponse("<h1>Додати пост</h1>")

def contacts(request):
    data = {
        'title': 'Контакти',
        'menu': menu,
        'menu_selected': 'contacts'
    }
    return HttpResponse("<h1>Контакти</h1>")

def login(request):
    data = {
        'title': 'Увійти',
        'menu': menu,
        'menu_selected': 'login'
    }
    return HttpResponse("<h1>Увійти</h1>")

def show_category(request, category_slug):
    category = get_object_or_404(Category, slug = category_slug)
    posts = Post.published.filter(category_id = category.pk).select_related('category')
    data = {
        'title': 'За категорією',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk
    }

    return render(request, 'blog/index.html', context=data)

def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Post.Status.PUBLISHED).select_related('category')
    data = {
        'title': f'Тег {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
        'tag_selected': tag.pk  # передайте первинний ключ (pk) тега
    }
    print(data['tag_selected'])
    return render(request, 'blog/index.html', context=data)
