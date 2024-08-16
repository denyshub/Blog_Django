menu = [{'title':'Головна', 'url': 'home' }, { 'title':'Додати статтю', 'url': 'add_post'},  {'title':'Про сайт', 'url': 'about' },{'title':'Зворотній зв\'язок', 'url':'contacts'}]

class DataMixin:
    title_page = None
    extra_context = {}
    menu_selected = None
    cat_selected = None
    paginate_by = 5
    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu


    def get_mixin_context(self, context, **kwargs):
        context['cat_secelcted'] = None
        context['menu'] = menu
        context.update(kwargs)

        return context
