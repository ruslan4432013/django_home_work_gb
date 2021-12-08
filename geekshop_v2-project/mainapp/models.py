from django.db import models


# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=14, unique=True)
    descriptions = models.TextField(verbose_name='Описание продукта', blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(verbose_name='Имя продукта', max_length=128)
    image = models.ImageField(verbose_name='Картинка', upload_to='img/', blank=True)
    short_desc = models.CharField(verbose_name='Краткое описание', max_length=60, blank=True)
    descritpion = models.TextField(verbose_name='Описание продукта', blank=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=5, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='Сколько на складе', default=0)

    def __str__(self):
        return f'{self.name} ({self.category})'
