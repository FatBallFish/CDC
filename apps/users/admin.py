from django.contrib import admin
from django.utils.html import format_html

from apps.users.models import JpaUsers


# Register your models here.
@admin.register(JpaUsers)
class JpaUsersAdmin(admin.ModelAdmin):
    # 编辑界面
    fieldsets = (
        ("基本信息", {'fields': ('username', 'nickname', 'phone', 'email', 'age')}),
        ("其他信息", {"fields": ("image", "create_time", "last_modified_time")}),
        ("隐私信息", {"fields": ("password", "salt", "real_auth_id", "is_active")})
    )

    def read_img(self, faces_data):
        if faces_data.if_local == True:
            return format_html('<img src="/media/{}" style="width:100px;height:auto">', faces_data.pic)
        else:
            return format_html('<img src="{}" style="width:100px;height:auto">', faces_data.cos_pic)

    read_img.short_description = "用户头像"
    # 显示界面
    list_display = ('username', 'phone', 'email', 'is_active', 'create_time', 'last_modified_time')  # 列表中显示的字段
    # list_display_links = list_display  # 列表中可点击跳转的字段
    list_display_links = list_display  # 列表中可点击跳转的字段
    # list_editable = ('content', 'sex', 'faces_group')  # 列表中可编辑的字段,注意：list_display_links与list_editable不可使用相同字段
    # 上面那个有点难看，取消

    search_fields = ('username', 'nickname', "phone", 'email')  # 列表搜索字段
    list_filter = ('is_active', 'create_time', 'last_modified_time')  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100
