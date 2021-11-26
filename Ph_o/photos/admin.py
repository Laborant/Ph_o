from django.contrib import admin
from .models import Photo, Category, RunUser, Tags, PhotoToBuy, Invoice
# Register your models here.

admin.site.register(Photo)
admin.site.register(Category)
admin.site.register(RunUser)
admin.site.register(Tags)
admin.site.register(PhotoToBuy)
admin.site.register(Invoice)

class PhotoAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'tag', 'created']
    list_filter = ['tag']