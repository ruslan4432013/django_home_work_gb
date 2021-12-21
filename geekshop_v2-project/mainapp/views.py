from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from .models import Product, ProductCategory

menu = [
    {'href': 'index', 'name': 'главная'},
    {'href': 'products:index', 'name': 'продукты'},
    {'href': 'contact', 'name': 'контакты'},
]


# Create your views here.

def products(request, pk=None):
    print(pk)
    title = "Продукты"
    links_menu = ProductCategory.objects.all()

    basket = []

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        content = {

            "title": title,
            "links_menu": links_menu,
            "category": category,
            "products": products,
            "menu": menu,
            "basket": basket,
        }

        return render(request, "mainapp/products_list.html", content)
    same_products = Product.objects.all()[3:5]

    content = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products,
        'menu': menu,
        "basket": basket,
    }

    return render(request, 'mainapp/products.html', content)


def contact(request):
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    content = {
        'title': 'Контакты',
        'menu': menu,
        'basket': basket,
    }
    return render(request, 'mainapp/contact.html', content)


def main(request):
    title = 'главная'
    products = Product.objects.all()[:4]
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    content = {'title': title,
               'products': products,
               'menu': menu,
               'basket': basket}
    return render(request, 'mainapp/index.html', content)
