import os, uuid

from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from blog.forms import AddPostForm, UploadFileForm
from blog.models import Post, Category, TagPost, UploadFile
from blog.utils import DataMixin


class BlogHome(DataMixin, ListView):
    template_name = 'blog/index.html'
    #model = Post
    context_object_name = 'posts'
    title_page= 'Головна сторінка'
    menu_selected = 'home'
    cat_selected = 0
    paginate_by = 5

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


class ShowPost(DataMixin, DetailView):
    template_name = 'blog/post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)



    def get_object(self, queryset=None):
        return get_object_or_404(Post.published, slug=self.kwargs[self.slug_url_kwarg])

class AddPage(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'blog/addpage.html'
    title_page = 'Додати пост'
    menu_selected = 'add_post'



class UpdatePage(DataMixin, UpdateView):
    model = Post
    title_page = 'Редагувати пост'
    fields = ['title', 'image', 'content','is_published', 'category', 'tags']
    template_name = 'blog/addpage.html'
    success_url = reverse_lazy('home')


class DeletePage(DataMixin, DeleteView):
    model = Post
    title_page =  'Видалити пост'
    fields = ['title', 'image', 'content', 'is_published', 'category', 'tags']
    template_name = 'blog/addpage.html'
    success_url = reverse_lazy('home')



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
        'menu_selected': 'login'
    }
    return HttpResponse("<h1>Увійти</h1>")

class PostCategory(DataMixin, ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Post.published.filter(category__slug=self.kwargs['category_slug']).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context['posts'][0].category
        return self.get_mixin_context(context, title = 'Категорія - ' + category.name , cat_selected = category.pk)


class PostTags(DataMixin, ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    allow_empty = False
    def get_queryset(self):
        return Post.published.filter(tags__slug=self.kwargs['tag_slug'])

    def get_context_data(self, **kwargs):
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title='Тег - ' + tag.tag, tag_selected=tag.pk)
