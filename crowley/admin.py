from django.contrib import admin

from .models import Crawler, Tag


class CrawlerAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    list_filter = ['active']
    search_fields = ['name']


class TagAdmin(admin.ModelAdmin):
    list_display = ('content', 'action', 'active')
    list_filter = ['action', 'active']
    search_fields = ['content']


admin.site.register(Crawler, CrawlerAdmin)
admin.site.register(Tag, TagAdmin)
