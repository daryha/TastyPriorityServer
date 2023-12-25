from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

from django.contrib.auth.models import User
from django.conf import settings

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_image_resolution(image):
    required_width = 200
    required_height = 200

    if image.width != required_width or image.height != required_height:
        raise ValidationError(
            _('Изображение должно быть ровно %sx%s пикселей.' % (required_width, required_height))
        )

def validate_image_filesize(image):
    max_size = 1024 * 1024 * 2  # 2MB
    if image.file.size > max_size:
        raise ValidationError(_('Максимальный размер файла должен быть менее 2MB.'))


class Store(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='image/')  # Баннер для магазина
    banner = models.ImageField(upload_to='store_banners/', blank=True, null=True)
    store_type = models.CharField(max_length=100)
    delivery_time = models.IntegerField()  # время доставки в минутах
    rating = models.FloatField()  # рейтинг магазина
    slug = models.SlugField(unique=True, default='')
    
    

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Store, self).save(*args, **kwargs)

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='store_image/')  # Баннер для магазина
    banner = models.ImageField(upload_to='store_banners/', blank=True, null=True)
    store_type = models.CharField(max_length=100)
    delivery_time = models.IntegerField()  # время доставки в минутах
    rating = models.FloatField()  # рейтинг магазина
    slug = models.SlugField(unique=True, default='')
   

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/')  # Изображение для категории
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='categories')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='categories', null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', validators=
        [
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            validate_image_resolution,
            validate_image_filesize,
        ])  # Изображение для продукта
    

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2)  # Вес продукта
    unit = models.CharField(max_length=10)  # Единица измерения, например, 'kg', 'lbs', 'pack', etc.

    def __str__(self):
        return self.name


#Basket
    

