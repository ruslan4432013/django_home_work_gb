from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from basketapp.models import Basket
from mainapp.models import Product


def basket(request):
    pass

def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity +=1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # Возвращает на ту же страницу, где находится

def basket_remove(request, pk):
    pass