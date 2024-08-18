import os, uuid

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from blog.forms import AddPostForm, UploadFileForm
from blog.models import Post, Category, TagPost, UploadFile
from blog.utils import DataMixin

from django.db.models import Q

class ArticleSearchView(DataMixin, ListView):
    model = Post
    template_name = 'blog/index.html'  # Зазначте ваш шаблон тут
    context_object_name = 'posts'
    title_page = 'Результати пошуку'
    def get_queryset(self):

        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context

class BlogHome(DataMixin, ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    title_page = 'Головна сторінка'
    menu_selected = 'home'
    cat_selected = 0

    def get_queryset(self):
        return Post.published.all().select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.get_mixin_context(context)
        return context


class AboutPage(DataMixin, TemplateView):
    template_name = 'blog/about.html'
    menu_selected = 'about'
    title_page = 'Про нас'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.get_mixin_context(context)
        return context


class ShowPost(DataMixin, DetailView):
    template_name = 'blog/post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'
    menu_selected = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Post.published, slug=self.kwargs[self.slug_url_kwarg])



class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'blog/addpage.html'
    title_page = 'Додати пост'
    menu_selected = 'add_post'
    permission_required = 'blog.add_post'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.get_mixin_context(context)
        return context

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Post
    title_page = 'Редагувати пост'
    fields = ['title', 'image', 'content', 'is_published', 'category', 'tags']
    template_name = 'blog/addpage.html'
    success_url = reverse_lazy('home')
    permission_required = 'blog.change_post'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Post.objects.all()
        return Post.objects.filter(author=self.request.user)


class DeletePage(PermissionRequiredMixin, DataMixin, DeleteView):
    model = Post
    title_page = 'Видалити пост'
    template_name = 'blog/addpage.html'
    success_url = reverse_lazy('home')
    permission_required = 'blog.delete_post'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Post.objects.all()
        return Post.objects.filter(author=self.request.user)


class PostCategory(DataMixin, ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Post.published.filter(category__slug=self.kwargs['category_slug']).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context['posts'][0].category
        return self.get_mixin_context(context, title='Категорія - ' + category.name , cat_selected = category.pk)


def page_not_found(request, exception):
    return HttpResponseNotFound("Сторінку не знайдено")

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
