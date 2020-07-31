from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from django.db.models import Q

from apps.community.resources import CommunityResource
from apps.community.models import Community


# Register your models here.

@admin.register(Community)
class CommunityAdmin(ImportExportActionModelAdmin):
    fieldsets = (
        ("基本信息", {'fields': ('id', 'sender', 'content')}),
        ("商品信息", {"fields": ("item",)}),
        ("时间信息", {"fields": ("add_time", "update_time")}),
        ("地理信息", {"fields": ("latitude", "longitude")}),
    )
    readonly_fields = ('id',)
    list_display = (
        'id', 'sender', 'content', 'item', 'add_time', 'update_time', "latitude", "longitude")
    list_display_links = list_display
    search_fields = ('id', 'sender', 'content')
    list_filter = ('sender', 'item', 'add_time', 'update_time')
    list_per_page = 20
    resource_class = CommunityResource
