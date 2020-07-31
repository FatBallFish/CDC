from django.contrib import admin
from django.db.models import Q
from import_export.admin import ImportExportActionModelAdmin

from apps.orders.resources import JpaOrderformResource
from apps.orders.models import JpaOrderform
from apps.products.models import JpaStores


# Register your models here.

@admin.register(JpaOrderform)
class JpaOrderformAdmin(ImportExportActionModelAdmin):
    resource_class = JpaOrderformResource

    fieldsets = (
        ("基本信息", {'fields': ('id', 'serial_number', 'store', 'item', 'item_num', 'username')}),
        ("详细信息",
         {"fields": (
             "item_price", "real_price", "pay_status", "transport_status")}),
        ("时间信息", {"fields": ("createtime", "cancle_time", "pay_time", "send_time", "refund_time")}),
    )
    # readonly_fields 的数据到下面处理，这里写没用
    list_display = (
        'id', 'serial_number', 'store', "item", 'item_num', 'username', 'real_price', 'createtime', 'pay_status')
    list_display_links = list_display
    search_fields = ('id', 'serial_number', 'store__id', 'item__id', 'username')
    list_filter = (
        'store_id', 'item_id', 'createtime', 'pay_status')
    list_per_page = 20

    def get_queryset(self, request):
        qs = super(JpaOrderformAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        # print(request.user.username)
        store_list = JpaStores.objects.filter(owner_name=request.user.username)
        condition = Q()
        for store in store_list:
            condition = condition | Q(store=store)
        return qs.filter(condition)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ["id"]
        if not request.user.is_superuser:
            readonly_fields.extend(["store_id", "create_time", "lastmodified_time", "read_item_portrait"])

        return readonly_fields

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            if obj.username == request.user.username:
                return True
        if request.user.is_superuser:
            return True
        return False
