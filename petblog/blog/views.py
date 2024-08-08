from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from blog.models import Post, Category

menu = [{'title':'Головна', 'url': 'home' }, {'title':'Про сайт', 'url': 'about' }, { 'title':'Додати статтю', 'url': 'add_page'},{'title':'Зворотній зв\'язок', 'url':'contacts'}]

data_db = [
    {'id': 1, 'title': 'Новини дня', 'content': "«Провів Ставку. Питання номер один – ситуація на фронті. Особливо детально – Покровський, Торецький і Харківський напрямки. Головком Олександр Сирський доповідав по відеозв'язку: він зараз на місці й тримає ситуацію під особистим контролем». Також на Ставці були доповіді військової та зовнішньої розвідок щодо прогнозів розвитку ситуації та найближчих цілей російських військ. Крім того, обговорили українське виробництво дронів і ракет, його динаміку та потребу в них Сил оборони до кінця року. Були доповіді міністра оборони Рустема Умєрова, віцепрем’єра з інновацій Михайла Федорова та міністра з питань стратегічних галузей промисловості Олександра Камишіна. Також рішенням Ставки спрямували додаткове фінансування на українську ракетну програму. «Ракет власного виробництва буде більше», - наголосив Президент. Він додав, що ще одна доповідь Умєрова стосувалася насичення зброєю та технікою додаткових бригад. Зараз над цим питанням активно працюють із партнерами.", "is_published": True},
    {'id': 2, 'title': 'Ігри', 'content': "Ми майже здолали того боса, але потім він використав своє АОЕ і вбив усю нашу групу!– скаже вам фанат WoW після невдалого рейду. В повсякденному житті вигадати використання цьому терміну важко, але можливо. До прикладу, якщо в дощовий день машина обляпала усіх, хто стояв на зупинці, то це цілком можна назвати \"АОЕ\". Звідки походить термін? Термін виник з настільних рольових ігор, таких як Dungeons & Dragons, де він так само використовувався для опису заклять і ефектів, що впливають на певну площу на ігровому полі. Коли ці механіки почали впроваджуватись у відеоігри, особливо в RPG та стратегії, то й \"AOE\" теж перекочувало до відеоігрової термінології.", "is_published": True},
    {'id': 3, 'title': 'Прогулянка', 'content': "Києво-Печерська лавра. Найвідоміший монастир Східної Європи, святиня для будь-якого християнина, перша обитель монахів на Русі, пам'ятник під захистом ЮНЕСКО. Краса її храмів торкнеться серця найзатятішого атеїста. Пройтися вздовж стародавніх стін, зайти в кожну будівлю, щоб попросити здоров'я для рідних, світу для країни, а потім опуститися в загадкові печери, намагаючись усвідомити, наскільки вони давні та як багато побачили – ось короткий маршрут для самостійної пішої прогулянки цим святим місцем Києва . На території Лаври знаходиться величезний музейний комплекс. Що тут робити та де варто погуляти? Екскурсійна мапа Києва підкаже, куди можна зайти. Це Музей золота та коштовностей, де представлені унікальні зразки скіфського золота. Вражає різноманітністю експонатів Музей народного мистецтва. Змусить завмерти Музей голограм, серед експонатів якого коштовності давньої Русі, ікони, церковне начиння, інше. Звичайно, все це голограми.", "is_published": True},
]

categories_db = [
    {'id': 1, "name": 'Ігри'},
    {'id': 2, 'name': 'Новини'},
    {'id': 3, 'name':'Подорожі'},
    {'id': 4, 'name': 'Мода'},
    
    ]


def index(request):
    posts = Post.published.all()
    data = {
        'title': 'Головна сторінка',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
        'menu_selected': 'home'
            }
    return render(request, 'blog/index.html', context = data)

def about(request):
    data = {
        'title': 'Про сайт',
        'menu': menu,
        'menu_selected': 'about'
    }
    return render(request, 'blog/about.html', context = data)

def archive(request, year):
    if year > 2024:
        url = reverse('categories', args=('games',))
        return redirect(url)
    return HttpResponse(f'<h1>Архів {year} року</h1>')


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Сторінка не знайдена</h1>" )

def show_post(request, post_slug):
    post = get_object_or_404(Post, slug = post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1
    }

    return render(request, 'blog/post.html', context=data)

def add_page(request):
    data = {
        'title': 'Додати пост',
        'menu': menu,
        'menu_selected': 'add_post'
    }
    return HttpResponse("<h1>Додати пост</h1>")

def contacts(request):
    data = {
        'title': 'Контакти',
        'menu': menu,
        'menu_selected': 'contacts'
    }
    return HttpResponse("<h1>Контакти</h1>")

def login(request):
    data = {
        'title': 'Увійти',
        'menu': menu,
        'menu_selected': 'login'
    }
    return HttpResponse("<h1>Увійти</h1>")

def show_category(request, category_slug):
    category = get_object_or_404(Category, slug = category_slug)
    posts = Post.published.filter(category_id = category.pk)
    data = {
        'title_':f'Категорія {category.name}',
        'title': 'За категорією',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk
    }

    return render(request, 'blog/index.html', context=data)