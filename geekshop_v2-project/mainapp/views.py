from django.shortcuts import render, get_object_or_404
import random
from basketapp.models import Basket
from .models import Product, ProductCategory

menu = [
    {'href': 'index', 'name': 'главная'},
    {'href': 'products:index', 'name': 'продукты'},
    {'href': 'contact', 'name': 'контакты'},
]


# Create your views here.
def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []

def get_hot_product():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]

def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products



def products(request, pk=None):
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

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': title,
        'links_menu': links_menu,
        'hot_product': hot_product,
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

def product(request, pk):
    title = 'продукты'

    content = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/product.html', content)