from django import  template
import blog.views as views

register = template.Library()

@register.simple_tag()
def get_categories():
    return views.categories_db