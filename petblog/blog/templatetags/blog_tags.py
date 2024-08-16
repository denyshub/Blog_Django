from django import  template
from django.db.models import Count, Q

import blog.views as views
from blog.models import Category, TagPost

register = template.Library()


@register.inclusion_tag('blog/list_categories.html')
def show_categories(cat_selected = 0):
    cats = Category.objects.annotate(
    total=Count('posts', filter=Q(posts__is_published=True))
).filter(total__gt=0)  
    return {'categories': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('blog/list_tags.html')
def show_all_tags(tag_selected = 0):
    tags = TagPost.objects.annotate(
    total=Count('tags', filter=Q(tags__is_published=True))
).filter(total__gt=0)
    return {'tags': tags, 'tag_selected': tag_selected}

