from django.db import models

from django.urls import reverse

from django_resized import ResizedImageField

from django.contrib.auth.models import User
class Category(models.Model):

    name = models.CharField(max_length=250, db_index=True)

    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):

        return reverse('list-category', kwargs={'slug': self.slug})


class Product(models.Model):

    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, null=True)

    title = models.CharField(max_length=250)

    brand = models.CharField(max_length=250, default='un-branded')

    descriptions = models.TextField(blank=True)

    slug = models.SlugField(max_length=255)

    price = models.DecimalField(max_digits=4, decimal_places=2)

    image = ResizedImageField(size=[None, 500], upload_to='images/')

    class Meta:
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title

    def get_absolute_url(self):

        return reverse('product-info', kwargs={'slug': self.slug})

