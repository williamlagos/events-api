from django.contrib import admin
from .models import Event, Owner


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'place_city', 'start_time', 'status',
                    'is_page_owned', 'active')
    list_filter = ['start_time', 'status', 'place_state', 'place_city',
                   'is_page_owned', 'origin', 'active']
    search_fields = ['name', 'description', 'start_time']
    list_per_page = 50


class OwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner_type', 'active')
    list_filter = ['owner_type', 'active']
    search_fields = ['name']
    list_per_page = 50


admin.site.register(Event, EventAdmin)
admin.site.register(Owner, OwnerAdmin)
