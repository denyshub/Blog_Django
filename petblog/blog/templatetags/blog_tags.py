from django import  template
import blog.views as views
from blog.models import Category

register = template.Library()


@register.inclusion_tag('blog/list_categories.html')
def show_categories(cat_selected = 0):
    cats = Category.objects.all()
    return {'categories': cats, 'cat_selected': cat_selected}

