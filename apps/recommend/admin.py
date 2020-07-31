import json

from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from apps.recommend.models import JpaItemUserBehavior
from apps.recommend.resources import JpaItemUserBehaviorResource




# Register your models here.


@admin.register(JpaItemUserBehavior)
class JpaItemUserBehaviorAdmin(ImportExportActionModelAdmin):
    fieldsets = (
        ("商品信息", {'fields': ('id', 'item_id', 'item_type')}),
        ("用户信息", {"fields": ("username", "behavior_type", "user_geohash")}),
        ("其他信息", {"fields": ("happen_time",)})
    )
    list_display = (
        'id', 'item_id', 'item_type', 'username', 'behavior_type', 'user_geohash', 'happen_time')
    readonly_fields = ('id',)
    list_display_links = list_display
    search_fields = ('item_id', 'username')
    list_filter = ('item_type', 'behavior_type', 'happen_time')
    list_per_page = 20
    # resource
    resource_class = JpaItemUserBehaviorResource
