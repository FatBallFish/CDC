from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from apps.recommend.models import JpaItems, JpaItemUserBehavior, JpaStores

from apps.recommend.resources import JpaStoresResource, JpaItemsResource, JpaItemUserBehaviorResource


# Register your models here.

@admin.register(JpaStores)
class JpaStoresAdmin(ImportExportActionModelAdmin):
    fieldsets = (
        ("基本信息", {'fields': ('id', 'name', 'owner_name', 'is_active')}),
        ("详细信息", {"fields": ("portrait", "store_index", "des", "tag",)}),
        ("地区信息", {"fields": ("district", "address")}),
        ("时间信息", {"fields": ("create_time", "lastmodified_time")})
    )
    list_display = (
        'id', 'name', 'owner_name', 'is_active', 'des', 'create_time', 'lastmodified_time')
    list_display_links = list_display
    search_fields = ('name', 'owner_name', 'des', 'tag')
    list_filter = ('is_active', 'district', 'address', 'create_time', 'lastmodified_time')
    list_per_page = 20

    # resource
    resource_class = JpaStoresResource


@admin.register(JpaItems)
class JpaItemsAdmin(ImportExportActionModelAdmin):
    fieldsets = (
        ("基本信息", {'fields': ('id', 'item_name', 'store_id', 'item_type')}),
        ("详细信息", {"fields": ("item_des", "item_portrait", "item_status", "original_price", "discount_price")}),
        ("其他信息",
         {"fields": ("item_stock", "item_geohash")}),
        ("时间信息", {"fields": ("create_time", "lastmodified_time")})
    )
    list_display = (
        'id', 'item_name', 'item_status', 'item_portrait', 'store_id', 'original_price', 'discount_price', 'item_stock',
        'lastmodified_time')
    list_display_links = list_display
    search_fields = ('item_name', 'item_des')
    list_filter = (
        'store_id', 'item_type', 'item_status', 'original_price', 'discount_price', 'item_stock', 'create_time',
        'lastmodified_time')
    list_per_page = 20

    # resource
    resource_class = JpaItemsResource


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
