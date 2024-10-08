from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post, Category, TagPost


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ['id', 'title','slug','image','show_image', 'content','is_published', 'category', 'tags']
    readonly_fields = ['id', 'show_image', 'slug']

    list_display = ('id', 'title', 'show_image', 'time_create','is_published', 'category')

    filter_horizontal = ['tags',]
    list_display_links = ( 'title',)
    ordering = ['-time_create', 'title']
    list_editable = ('is_published',)
    list_per_page = 10
    save_on_top = True
    actions = [
        'set_published',
        'set_draft'
    ]
    search_fields = ['title','category__name']
    list_filter = ['category__name', 'is_published']
    @admin.display(description='Мініатюра')
    def show_image(self, post:Post):
        if post.image:
            return mark_safe(f"<img src='{post.image.url}' width=50>")
        else:
            "Немає зображення"
    @admin.action(description='Опублікувати')
    def set_published(self, request, queryset):
        count = queryset.update(is_published = Post.Status.PUBLISHED)
        self.message_user(request, f'Опубліковано {count} статей.')

    @admin.action(description='Приховати')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Post.Status.DRAFT)
        self.message_user(request, f'Приховано {count} статей.')
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    list_display_links = ('id', 'name')

@admin.register(TagPost)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id','tag')
    list_display_links = ('id', 'tag')
