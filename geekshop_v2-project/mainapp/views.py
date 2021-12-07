from django.shortcuts import render
from .models import Product, ProductCategory

menu = [
    {'href': 'index', 'name': 'главная'},
    {'href': 'products:index', 'name': 'продукты'},
    {'href': 'contact', 'name': 'контакты'},
]


# Create your views here.
def index(request):
    context = {'title': 'Магазин', 'menu': menu}
    return render(request, 'mainapp/index.html', context)


def products(request, pk=None):
    title = "Продукты"
    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]
    products = Product.objects.all().order_by('price')
    content = {
        "title": title,
        "links_menu": links_menu,
        "products": products,
        "menu": menu,
    }
    return render(request, 'mainapp/products.html', content)


def contact(request):
    content = {
        'title': 'Контакты',
        'menu': menu,
    }
    return render(request, 'mainapp/contact.html', content)


def main(request):
    title = 'главная'
    products = Product.objects.all()[:4]
    content = {'title': title, 'products': products, 'menu': menu}
    return render(request, 'mainapp/index.html', content)
