from django import forms
from .models import Category

class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, label='Заголовок: ')
    slug = forms.SlugField(max_length=255, label='URL(Необов\'язково): ', required=False)
    content = forms.CharField(widget=forms.Textarea(), required=False, label='Вміст: ')
    is_published = forms.BooleanField(required=False, label='Статус: ', initial=True)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категорія: ', empty_label='Категорія не обрана')
