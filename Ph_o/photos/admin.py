from django.contrib import admin
from .models import Photo, Category, RunUser
# Register your models here.

admin.site.register(Photo)
admin.site.register(Category)
admin.site.register(RunUser)

class PhotoAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'tag', 'created']
    list_filter = ['tag']