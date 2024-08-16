from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.db.models import Count, Q
from django.template.defaultfilters import slugify
from django.urls import reverse


def translit_to_english(text):
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ie',
        'ж': 'zh', 'з': 'z', 'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l',
        'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ю': 'iu', 'я': 'ia',
        'ь': '', '’': '', ' ': '-',
    }

    return "".join(map(lambda x: translit_dict[x] if translit_dict.get(x, False) else x, text.lower()))


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published = Post.Status.PUBLISHED)

class NotEmptyCategory(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            num_published_posts=Count('post', filter=Q(post__is_published=True))
        ).filter(num_published_posts__gt=0)

class Post(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0
        PUBLISHED = 1

    title = models.CharField(max_length=255,verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True,  validators=[
        MinLengthValidator(5, message='Мінімум 5 символів'),
        MaxLengthValidator(100, message='Максимум 100 символів'),
    ],)
    image = models.ImageField(upload_to='images/%Y/%m/%d', default=None, blank=True, null=True, verbose_name = 'Фото')
    content = models.TextField(blank=True,verbose_name='Вміст')
    time_create = models.DateTimeField(auto_now_add=True,verbose_name='Дата створення')
    time_update = models.DateTimeField(auto_now=True,verbose_name='Дата зміни')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]),x[1]), Status.choices)), default=Status.PUBLISHED,verbose_name='Статус')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts',verbose_name='Категорія')
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags',verbose_name='Теги')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True, default=None)
    objects = models.Manager()
    published = PublishedManager()
    def __str__(self):
        return self.title

    class Meta():
        verbose_name = 'Пост'
        verbose_name_plural = 'Пости'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = self.slug if self.slug else slugify(translit_to_english(self.title))
        super().save(*args, **kwargs)

    


class Category(models.Model):
    name = models.CharField(max_length=100,verbose_name='Категорія')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta():
        verbose_name = 'Категорію'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    objects = models.Manager()
    not_empty = NotEmptyCategory()


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

class UploadFile(models.Model):
    file = models.FileField(upload_to='uploads_model')