from django.shortcuts import render

# Create your views here.

links_menu = [
    {'href': 'products_all', 'name': 'все'},
    {'href': 'products_home', 'name': 'дом'},
    {'href': 'products_office', 'name': 'офис'},
    {'href': 'products_modern', 'name': 'модерн'},
    {'href': 'products_classic', 'name': 'классика'},
]

links_main_menu = [
    {'href': 'index', 'name': 'домой'},
    {'href': 'products', 'name': 'продукты'},
    {'href': 'contact', 'name': 'контакты'},

]


def index(request):
    content = {
        'title': 'Главная',
        'links_main_menu': links_main_menu
    }
    return render(request, 'mainapp/index.html', content)


def products(request):
    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
        'links_main_menu':  links_main_menu
    }
    return render(request, 'mainapp/products.html', content)


def contact(request):
    content = {
        'title': 'Контакты',
        'links_main_menu': links_main_menu
    }
    return render(request, 'mainapp/contact.html', content)


def context(request):
    content = {
        'title': 'Магазин',
        'header': 'Welcome to site',
        'username': 'Ivan Ivanov',
        'products': [
            {'name': 'Стулья', 'price': 4535},
            {'name': 'Диваны', 'price': 45305},
            {'name': 'Кровати', 'price': 7835}
        ]
    }
    return render(request, 'mainapp/test_context.html', content)
