import os, uuid

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q, Prefetch
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from blog.forms import AddPostForm
from blog.models import Post, TagPost
from blog.utils import DataMixin
from django.views.decorators.cache import cache_page
from django.core.cache import cache

@method_decorator(cache_page(60 * 15), name='dispatch')
class ArticleSearchView(DataMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    def get_queryset(self):
        query = self.request.GET.get('q')
        self.title_page = f'Результати пошуку: {query}'
        if query:
            return Post.objects.select_related('author', 'category').filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            ).distinct().defer('time_update','is_published','tags',)
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['query'] = self.request.GET.get('q', '')
        return context

@method_decorator(cache_page(60 * 15), name='dispatch')
class BlogHome(DataMixin, ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    title_page = 'Головна сторінка'
    menu_selected = 'home'
    cat_selected = 0

    def get_queryset(self):
        return Post.published.all().select_related('category', 'author').defer('time_update','is_published','tags',)

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

@method_decorator(cache_page(60 * 15), name='dispatch')
class ShowPost(DataMixin, DetailView):
    template_name = 'blog/post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'
    menu_selected = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Post.published.select_related('category', 'author').only('title', 'content', 'time_create','slug', 'category','author', 'image'), slug=self.kwargs[self.slug_url_kwarg])


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
        post = form.save(commit=False)
        post.author = self.request.user
        cache.clear()
        return super().form_valid(form)

@method_decorator(cache_page(60 * 15), name='dispatch')
class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Post
    title_page = 'Редагувати пост'
    fields = ['title', 'image', 'content', 'is_published', 'category', 'tags']
    template_name = 'blog/addpage.html'
    success_url = reverse_lazy('home')
    permission_required = 'blog.change_post'

    def get_queryset(self):
        cache.clear()
        queryset = Post.objects.select_related('category', 'author').all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(author=self.request.user)
        return queryset

@method_decorator(cache_page(60 * 15), name='dispatch')
class DeletePage(PermissionRequiredMixin, DataMixin, DeleteView):
    model = Post
    title_page = 'Видалити пост'
    template_name = 'blog/addpage.html'
    success_url = reverse_lazy('home')
    permission_required = 'blog.delete_post'

    def get_queryset(self):
        cache.clear()
        queryset = Post.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(author=self.request.user)
        return queryset

@method_decorator(cache_page(60 * 15), name='dispatch')
class PostCategory(DataMixin, ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Post.published.filter(category__slug=self.kwargs['category_slug']).select_related('category', 'author').defer('time_update','is_published','tags',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context['posts'][0].category
        return self.get_mixin_context(context, title='Категорія - ' + category.name, cat_selected=category.pk)


def page_not_found(request, exception):
    return HttpResponseNotFound("Сторінку не знайдено")

@method_decorator(cache_page(60 * 15), name='dispatch')
class PostTags(DataMixin, ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Post.published.filter(
            tags__slug=self.kwargs['tag_slug']
        ).select_related(
            'author', 'category'
        ).prefetch_related(
            'tags'
        ).defer(
            'time_update', 'is_published'
        )

    def get_context_data(self, **kwargs):
        tag = get_object_or_404(TagPost, slug=self.kwargs['tag_slug'])
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title='Тег - ' + tag.tag, tag_selected=tag.pk)
