from django.contrib import admin
from django.db.models import Q
from django.utils.html import format_html

from import_export.admin import ImportExportActionModelAdmin

from apps.products.resources import JpaItemsResource, JpaStoresResource
from apps.products.models import JpaItems, JpaStores

from extra_apps.tags.main import TfIdf
from datetime import datetime
from random import Random
import json


# Register your models here.

@admin.register(JpaStores)
class JpaStoresAdmin(ImportExportActionModelAdmin):
    fieldsets = (
        ("基本信息", {'fields': ('id', 'name', 'owner_name', 'is_active')}),
        ("详细信息", {"fields": ("portrait", "store_index", "des", "tag",)}),
        ("地区信息", {"fields": ("district", "address", "latitude", "longitude")}),
        ("时间信息", {"fields": ("create_time", "lastmodified_time")}),
    )
    list_display = (
        'id', 'name', 'owner_name', 'is_active', 'des', 'create_time', 'lastmodified_time', "latitude", "longitude")
    list_display_links = list_display
    search_fields = ('name', 'owner_name', 'des', 'tag')
    list_filter = ('is_active', 'district', 'address', 'create_time', 'lastmodified_time')
    list_per_page = 20
    # resource
    resource_class = JpaStoresResource

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            # 非管理员状态下，对店主字段进行约束
            obj.owner_name = request.user.username
        if not change:
            # 创建视图
            obj.create_time = datetime.now()
            obj.id = "{}{}".format(Random().randint(1000000000, 9999999999), request.user.username)
        else:
            pass
        # 无论什么情况下，最后操作时间一定要重新赋值
        obj.lastmodified_time = datetime.now()
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(JpaStoresAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        # print(request.user.username)
        return qs.filter(owner_name=request.user.username)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = []
        if not request.user.is_superuser:
            readonly_fields = ("id", "owner_name", "create_time", "lastmodified_time")

        return readonly_fields

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "is_active":
                # 非超级管理员状态下店铺状态只有以下几个状态可用
                kwargs["choices"] = ((0, "打烊"), (1, "营业中"), (3, "临时关店"))
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        # 判断店铺是否已注销或封禁或冻结，若真则只能查看
        if obj is not None:
            if obj.is_active in [2, 4, 5]:
                return False
        return True

    def has_add_permission(self, request):
        username = request.user.username
        condition = Q(owner_name=username) & ~Q(is_active=5)
        store_list = JpaStores.objects.filter(condition)
        if len(store_list) == 0:
            return True
        else:
            return False

    actions = ['close_store']

    def close_store(self, request, obj):
        # 关闭店铺时，将该店铺所属的所有商品设为已删除状态
        for o in obj.all():
            if o.is_active == 5:
                continue
            o.is_active = 5
            o.save()
            item_list = JpaItems.objects.filter(store_id=o.id)
            for item in item_list:
                item.item_status = 3
                item.save()

    close_store.short_description = "永久关闭店铺"
    close_store.type = "danger"
    close_store.confirm = '是否永久关闭店铺？关闭后该店铺所有的商品也将被删除。'


@admin.register(JpaItems)
class JpaItemsAdmin(ImportExportActionModelAdmin):
    fieldsets = (
        ("基本信息", {'fields': ('id', 'item_name', 'store_id', 'item_type')}),
        ("详细信息",
         {"fields": (
             "item_tags", "simple_desc", "item_des", "item_portrait", "read_item_portrait", "item_status",
             "original_price", "discount_price")}),
        ("其他信息",
         {"fields": ("item_stock", "item_geohash")}),
        ("时间信息", {"fields": ("create_time", "lastmodified_time")}),
    )
    # readonly_fields 的数据到下面处理，这里写没用
    list_display = (
        'id', 'item_name', 'item_type', "simple_desc", 'item_tags', 'item_status', 'read_item_portrait', 'store_id',
        'original_price',
        'discount_price',
        'item_stock',
        'lastmodified_time')

    def read_item_portrait(self, item):
        return format_html('<img src="{}" style="width:100px;height:auto">', item.item_portrait)

    read_item_portrait.short_description = "商品图片·显示"

    list_display_links = list_display
    search_fields = ('id', 'item_name', 'item_des', 'item_tags')
    list_filter = (
        'store_id', 'item_type', 'item_tags', 'item_status', 'original_price', 'discount_price', 'item_stock',
        'create_time',
        'lastmodified_time')
    list_per_page = 20

    # resource
    resource_class = JpaItemsResource

    def save_model(self, request, obj, form, change):
        if not change:
            # 创建视图
            # 约束创建时间，商品id，店铺id
            obj.create_time = datetime.now()
            rand = Random()
            while True:
                # 判断是否重复
                item_id = rand.randint(1000000000, 9999999999)
                try:
                    JpaItems.objects.get(id=item_id)
                except JpaItems.DoesNotExist as e:
                    break
            obj.id = item_id

            # 店铺id的处理机制是，当用户名下只有一家店铺时，使用该家店铺，否则随机选择一家
            username = request.user.username
            condition = Q(owner_name=username) & ~Q(is_active=5)
            store_list = JpaStores.objects.filter(condition)
            if len(store_list) > 0:
                store = store_list[0]
                obj.store_id = store.id
        else:
            pass
        # 无论什么情况下，最后操作时间一定要重新赋值
        obj.lastmodified_time = datetime.now()
        if obj.item_status == -1:
            obj.item_status = 0
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        # 自动筛选属于该用户的商品列表,
        qs = super(JpaItemsAdmin, self).get_queryset(request)
        store_list = JpaStores.objects.filter(owner_name=request.user.username)
        condition = Q()
        for store in store_list:
            condition = condition | Q(store_id=store.id)
        # 在这里不能设置已删除的筛选条件，会与外部的筛选条件冲突
        # condition = condition & Q(item_status=3)
        if request.user.is_superuser:
            return qs
        # print(request.user.username)
        return qs.filter(condition)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ["read_item_portrait"]
        if not request.user.is_superuser:
            readonly_fields.extend(["id", "store_id", "create_time", "lastmodified_time", "read_item_portrait"])

        return readonly_fields

    def has_change_permission(self, request, obj=None):
        # 判断商品是否已删除，若已删除则只能查看
        if obj is not None:
            if obj.item_status == 3:
                return False
        return True

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "item_status":
                # 非超级管理员状态下店铺状态只有以下几个状态可用
                kwargs["choices"] = ((1, "售卖中"), (2, "已下架"))
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    # 处理默认删除效果以及判断添加商品前是否有店铺
    def has_add_permission(self, request):
        username = request.user.username
        condition = Q(owner_name=username) & ~Q(is_active=5)
        store_list = JpaStores.objects.filter(condition)
        if len(store_list) != 1:
            return False
        return True

    actions = ["delete_item", "getTags"]

    def delete_item(self, request, obj):
        # 关闭店铺时，将该店铺所属的所有商品设为已删除状态
        for o in obj.all():
            if o.item_status == 3:
                continue
            o.item_status = 3
            o.save()

    delete_item.short_description = "删除商品"
    delete_item.type = "danger"
    delete_item.confirm = '是否删除商品？删除后不可恢复。'

    def getTags(self, request, obj):
        if request.user.is_superuser:
            for o in obj.all():
                if o.item_status == -1:
                    # 商品为信息未完善状态
                    continue
                tf = TfIdf(o.item_name)
                result_list = tf.doJob()
                o.item_tags = json.dumps(result_list[0], ensure_ascii=False)
                o.save()

    getTags.short_description = "提取Tags"
    getTags.confirm = '提取后将覆盖原tags内容'
