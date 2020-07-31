from django.contrib import admin
from django.utils.html import format_html

from apps.tokens.models import JpaTokens


# Register your models here.

@admin.register(JpaTokens)
class JpaTokensAdmin(admin.ModelAdmin):
    # 编辑界面
    fieldsets = (
        ("基本信息", {'fields': ('token', 'username', 'enduring', 'type')}),
        ("时间信息", {"fields": ("create_time", "expire_time")}),
        ("地理信息", {"fields": ("latitude", "longitude")})
    )
    # 显示界面
    list_display = (
        'token', 'username', 'enduring', 'type', 'create_time', 'expire_time', "latitude", "longitude")  # 列表中显示的字段
    # list_display_links = list_display  # 列表中可点击跳转的字段
    list_display_links = list_display  # 列表中可点击跳转的字段
    # list_editable = ('content', 'sex', 'faces_group')  # 列表中可编辑的字段,注意：list_display_links与list_editable不可使用相同字段
    # 上面那个有点难看，取消

    search_fields = ('token', 'username')  # 列表搜索字段
    list_filter = ('enduring', 'type', 'create_time', 'expire_time')  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100
