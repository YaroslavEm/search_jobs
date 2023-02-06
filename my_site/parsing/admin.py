from django.contrib import admin
from .models import *


class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class LanguageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class TestAdmin(admin.ModelAdmin):
    list_display = ('city', 'title', 'url')


admin.site.register(Vacancy)
admin.site.register(City, CityAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Error)
admin.site.register(Url)
