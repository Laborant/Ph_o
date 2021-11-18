from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User, AbstractUser
from django.contrib import admin

#Create your models here.

def generateUUID():
    return str(uuid4())

class Category(models.Model):
    id = models.CharField(max_length=225, unique=True, blank=False,
        null=False, default=uuid4, primary_key=True)
    name = models.CharField(max_length=100, null=False,
                            blank=False)
    created = models.DateTimeField(auto_now_add=True)
    hold_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Photo(models.Model):
    id = models.CharField(max_length=225, unique=True, blank=False, null=False,
        default=uuid4, primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    image = models.ImageField(null=False, blank=False)
    # description = models.TextField(null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    tags = models.ManyToManyField('Tags', verbose_name="Номера", blank=True)
    #tags = models.ForeignKey('Tags', blank=True, on_delete=models.PROTECT, related_name='images')
    slug = models.SlugField(max_length=150, unique=True, default=generateUUID)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    # last_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
        # return self.tags


class RunUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Админ'),
        ('customer', 'Клиент'),
        ('photographer', 'Фотограф'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, verbose_name='Роль', choices=ROLE_CHOICES, default='customer')

    # is_author = models.BooleanField(default=False)
    # first_name = models.TextField (blank=None)
    # bib_number = models.CharField(max_length=6)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


# class Order(models.Model):
#     amount = models.CharField(blank=False, null=False, max_length=22)

class Tags(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    # photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'

# class PotoTag(models.Model):
#     photo = models.ForeignKey(Photo, on_delete = models.CASCADE)
#     tags = models.ForeignKey(Tags, on_delete = models.CASCADE)