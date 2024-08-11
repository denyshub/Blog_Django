from django.apps import AppConfig


class BlogConfig(AppConfig):
    verbose_name = 'Блог'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
