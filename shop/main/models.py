from django.db import models
from django.contrib.auth import get_user_model

from mptt.models import MPTTModel, TreeForeignKey

from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit


User = get_user_model()


class Category(MPTTModel):
    name = models.CharField(max_length = 50, verbose_name='Название')
    slug = models.SlugField(max_length=25, unique=True)   
    parent = TreeForeignKey(
        'self', blank=True, null=True,
        related_name='children',
        on_delete=models.CASCADE,
        db_index = True
        )
    image = models.ImageField(upload_to='images/category/', verbose_name='Изображение')

    class MPTTMeta:
       order_insertion_by = ['name']

    class Meta:
        unique_together = ('slug', 'parent')
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):  
        full_path = [self.name]       
        k = self.parent       
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])


class Product(models.Model):
    name = models.CharField(max_length = 100, verbose_name='Название')
    slug = models.SlugField(max_length=25, unique=True)   
    price = models.PositiveIntegerField(verbose_name='Цена')
    original_image = models.ImageField(upload_to='images/product/')
    small_image =ImageSpecField(
        source='original_image', format='JPEG',
        options={'quality': 90}, processors=[ResizeToFit(50, 50)]
        )
    big_image =ImageSpecField(
        source='original_image', format='JPEG',
        options={'quality': 90}, processors=[ResizeToFit(640, 480)]
        )
    category = TreeForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Категория')
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукты"
        verbose_name_plural = "Продукты"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
    

class CartProduct(models.Model):
    cart = models.ForeignKey(
        Cart , null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='cartproduct',
        verbose_name='Корзина-Продукт'
    )
    product = models.ForeignKey(
        Product ,null=True,
        on_delete=models.CASCADE,
        related_name='cartproduct',
        verbose_name='Продукт')
    quantity = models.PositiveIntegerField(
        verbose_name='Количество'
    )
