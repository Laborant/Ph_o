from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User, AbstractUser
from django.contrib import admin
import random
import string
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
    # photos_price
    # price_for_photo

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

class Invoice(models.Model):
    user = models.ForeignKey(RunUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    identify_code = models.CharField(max_length=50, verbose_name='Уникальний код', null=True, blank=True)
    # photo_collection = models.ManyToManyField('PhotoCollection', verbose_name="Коллекция", blank=True)

    def save(self, *args, **kwargs):
        if not self.identify_code:
            code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(48))
            try:
                Invoice.objects.get(identify_code=code)
                code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(48))
                try:
                    Invoice.objects.get(identify_code=code)
                    code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(48))
                    try:
                        Invoice.objects.get(identify_code=code)
                    except Invoice.DoesNotExist:
                        self.identify_code = code
                except Invoice.DoesNotExist:
                    self.identify_code = code
            except Invoice.DoesNotExist:
                self.identify_code = code
        super(Invoice, self).save(*args, **kwargs)

    def __str__(self):
        if self.user:
            return f'{self.user.email}'
        return str(self.id)

    class Meta:
        verbose_name = 'Инвойс'
        verbose_name_plural = 'Инвойсы'


class PhotoToBuy(models.Model):
    user = models.ForeignKey(RunUser, on_delete=models.SET_NULL, null=True, blank=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True, blank=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, blank=True)
    is_bought = models.BooleanField(default=False)
    is_archive = models.BooleanField(default=False)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=11, decimal_places=2, default=0, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Фото на продажу'
        verbose_name_plural = 'Фотографии на продажу'

