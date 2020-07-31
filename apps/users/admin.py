from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.models import JpaUsers

from extra_apps import MD5

from random import Random


# Register your models here.
@admin.register(JpaUsers)
class JpaUsersAdmin(admin.ModelAdmin):
    # 编辑界面
    fieldsets = (
        ("账号信息", {'fields': ('username', 'read_password', 'password', "salt",)}),
        ("其他信息", {"fields": ('image', "read_img", 'nickname', 'email', 'gender')}),
        ("时间信息", {"fields": ("create_time", "last_login")}),
        ("隐私信息", {"fields": ("real_auth", 'face', 'phone', 'age')}),
        ('权限信息', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    readonly_fields = ("read_img", "read_password")

    def read_password(self, user):
        return user.password

    def read_img(self, user):
        return format_html('<img src="{}" style="width:100px;height:auto">', user.image)

    read_img.short_description = "头像显示"
    # 显示界面
    list_display = (
        'getImage', 'username', 'nickname', 'gender', 'phone', 'is_active', 'is_staff', 'is_superuser', 'create_time',
        'last_login')  # 列表中显示的字段
    # list_display_links = list_display  # 列表中可点击跳转的字段
    list_display_links = list_display  # 列表中可点击跳转的字段
    # list_editable = ('content', 'sex', 'faces_group')  # 列表中可编辑的字段,注意：list_display_links与list_editable不可使用相同字段
    # 上面那个有点难看，取消

    search_fields = ('username', 'nickname', "phone", 'email')  # 列表搜索字段
    list_filter = ('is_active', 'create_time', 'last_login')  # 列表筛选字段
    list_per_page = 10  # 列表每页最大显示数量，默认100

    def save_model(self, request, obj, form, change):
        if not change:
            # 创建视图
            if obj.salt is None or obj.salt == "":
                salt = ""
                for i in range(16):
                    salt += Random().choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
                print("rand salt:", salt)
                obj.salt = salt
        check_list = str(obj.password).split("$", 1)
        if len(check_list) != 2:
            salt = obj.salt
            password = obj.password
            hash = MD5.md5(password, salt)
            obj.password = "{}${}".format(salt, hash)
        else:
            if obj.salt is None or obj.salt == "":
                obj.salt = check_list[0]
        super(JpaUsersAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(JpaUsersAdmin, self).get_queryset(request)
        print(qs)
        if request.user.is_superuser:
            return qs
        return qs.filter(username=request.user.username)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ["read_img", "read_password"]
        if not request.user.is_superuser:
            readonly_fields.extend(["username", "real_auth_id", "is_active", "is_staff", "is_superuser"])
        return readonly_fields

    def get_fieldsets(self, request, obj=None):
        if not request.user.is_superuser:
            fieldsets = (
                ("账号信息", {'fields': ('username', 'read_password', 'password',), "description": "若要修改密码直接输入密码明文即可"}),
                ("其他信息", {"fields": ('image', "read_img", 'nickname', 'email', 'gender')}),
                ("时间信息", {"fields": ("create_time", "last_login")}),
                ("隐私信息", {"fields": ("real_auth_id", 'phone', 'age')}),
            )
            return fieldsets
        return super().get_fieldsets(request, obj)

    def get_list_display(self, request):
        if not request.user.is_superuser:
            list_display = (
                'getImage', 'username', 'nickname', 'gender', 'phone', 'last_login')
            return list_display
        return super().get_list_display(request)
