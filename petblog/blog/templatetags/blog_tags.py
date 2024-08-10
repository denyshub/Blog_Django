from django import  template
import blog.views as views
from blog.models import Category, TagPost

register = template.Library()


@register.inclusion_tag('blog/list_categories.html')
def show_categories(cat_selected = 0):
    cats = Category.objects.all()
    return {'categories': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('blog/list_tags.html')
def show_all_tags(tag_selected = 0):
    print(TagPost.objects.all())
    return {'tags': TagPost.objects.all(), 'tag_selected': tag_selected}

