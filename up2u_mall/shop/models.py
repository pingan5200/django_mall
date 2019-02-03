from django.db import models
from django.urls import reverse

# Create your models here.
# 商品，分类，
class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            unique=True)
    isHome = models.BooleanField(default=False)
    detail = models.CharField(max_length=200, default='类别详情')
    description = models.TextField(blank=True, default='类别详情介绍类别详情介绍类别详情介绍类别详情介绍类别详情介绍')
    image = models.ImageField(upload_to='categories/%Y/%m/%d', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '类别'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                        args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    description = models.TextField(blank=True, default="居家必备，老少通吃，特别好用，携带方便")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_old = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    isHome = models.BooleanField(default=False)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                        args=[self.id, self.slug])


class Slide(models.Model):
    image = models.ImageField(upload_to='slides/%Y/%m/%d',
                              blank=True, verbose_name='轮播图')
    url = models.URLField(verbose_name='地址')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name