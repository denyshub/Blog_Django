from django import  template
import blog.views as views

register = template.Library()

@register.simple_tag()
def get_categories():
    return views.categories_db


@register.inclusion_tag('blog/list_categories.html')
def show_categories(cat_selected = 0):
    cats = views.categories_db
    return {'categories': cats, 'cat_selected': cat_selected}