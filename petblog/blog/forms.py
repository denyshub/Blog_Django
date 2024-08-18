from ckeditor.widgets import CKEditorWidget
from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError


from .models import Category, TagPost, Post
from ckeditor.fields import RichTextField

from ckeditor.fields import RichTextField  # Переконайтеся, що CKEditor встановлений


class AddPostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категорія',
                                      empty_label='Категорія не обрана')
    slug = forms.SlugField(required=False, label='URL (необов\'язково)')
    content = forms.CharField(widget=CKEditorWidget())  # Використовуємо RichTextField безпосередньо

    class Meta:
        model = Post
        fields = ['title', 'image', 'slug', 'content', 'is_published', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.HiddenInput(),  # Якщо ви використовуєте CKEditor, видалите це
        }
        labels = {
            'title': 'Заголовок',
            'image': 'Фото',
            'content': 'Вміст',
            'is_published': 'Статус',
            'category': 'Категорія',
            'tags': 'Теги',
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 100:
            raise ValidationError('Довжина більша за 100 символів.')
        elif len(title) < 5:
            raise ValidationError('Довжина менша за 5 символів.')
        return title
class UploadFileForm(forms.Form):
    file = forms.FileField(label='Файл')
