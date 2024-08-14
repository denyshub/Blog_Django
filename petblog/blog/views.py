import os, uuid

from django.db.models import Count
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from blog.forms import AddPostForm, UploadFileForm
from blog.models import Post, Category, TagPost, UploadFile

menu = [{'title':'Головна', 'url': 'home' }, { 'title':'Додати статтю', 'url': 'add_post'},  {'title':'Про сайт', 'url': 'about' },{'title':'Зворотній зв\'язок', 'url':'contacts'}]

# def index(request):
#     posts = Post.published.all().select_related('category')
#     data = {
#         'title': 'Головна сторінка',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#         'menu_selected': 'home',
#         'tag_selected': 0
#             }
#     return render(request, 'blog/index.html', context = data)


class BlogHome(ListView):
    template_name = 'blog/index.html'
    #model = Post
    context_object_name = 'posts'

    extra_context =  {
        'title': 'Головна сторінка',
        'menu': menu,
        'cat_selected': 0,
        'menu_selected': 'home',
        'tag_selected': 0
        }

    def get_queryset(self):
        return Post.published.all().select_related('category')




def about(request):

    data = {
        'title': 'Про сайт',
        'menu': menu,
        'menu_selected': 'about',

    }

    return render(request, 'blog/about.html', context=data)



def archive(request, year):
    if year > 2024:
        url = reverse('categories', args=('games',))
        return redirect(url)
    return HttpResponse(f'<h1>Архів {year} року</h1>')


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Сторінка не знайдена</h1>" )

# def show_post(request, post_slug):
#     post = get_object_or_404(Post, slug = post_slug)
#     data = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': 1
#     }
#
#     return render(request, 'blog/post.html', context=data)


class ShowPost(DetailView):
    template_name = 'blog/post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['menu'] = menu
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Post.published, slug=self.kwargs[self.slug_url_kwarg])

class AddPage(View):

    def get(self, request):
        form = AddPostForm()
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')

        data = {
            'title': 'Додати пост',
            'menu': menu,
            'form': form,
            'menu_selected': 'add_post'
        }
        return render(request, 'blog/addpage.html', context=data)

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')

        data = {
            'title': 'Додати пост',
            'menu': menu,
            'form': form,
            'menu_selected': 'add_post'
        }
        return render(request, 'blog/addpage.html', context=data)



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

class PostCategory(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Post.published.filter(category__slug=self.kwargs['category_slug']).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context['posts'][0].category
        context['title'] = 'Категорія - ' + category.name
        context['menu'] = menu
        context['cat_selected'] = category.pk
        context['menu_selected'] = ''
        return context


class PostTags(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Post.published.filter(tags__slug=self.kwargs['tag_slug'])

    def get_context_data(self, **kwargs):
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context = super().get_context_data(**kwargs)
        context['title'] = 'Тег - ' + tag.tag
        context['menu'] = menu
        context['tag_selected'] = tag.pk
        return context