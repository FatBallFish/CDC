from django.contrib import admin

from apps.realauth.models import JpaRealauth


# Register your models here.
@admin.register(JpaRealauth)
class JpaRealauthAdmin(admin.ModelAdmin):
    list_display = ['real_auth_id', 'name', 'gender', 'address', 'birthday', 'nation']

# admin.site.register(JpaRealauth)
