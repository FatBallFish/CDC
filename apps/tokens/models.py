from django.db import models

from apps.users.models import JpaUsers

from datetime import datetime, timedelta
from typing import Tuple


# Create your models here.

class JpaTokens(models.Model):
    token = models.CharField(verbose_name="token", primary_key=True, max_length=64)
    create_time = models.DateTimeField(verbose_name="创建时间", default=datetime.now)
    username = models.CharField(verbose_name="用户名", max_length=20, blank=True, null=True)
    enduring = models.CharField(verbose_name="是否长效", max_length=1, blank=True, null=True)
    expire_time = models.DateTimeField(verbose_name="过期时间", blank=True, null=True)
    type = models.CharField(verbose_name="类型", max_length=1, blank=True, null=True)
    latitude = models.DecimalField(verbose_name="纬度", max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(verbose_name="经度", max_digits=10, decimal_places=7, blank=True, null=True)

    class Meta:
        verbose_name = "token"
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'jpa_tokens'

    def __str__(self):
        return "{}({})".format(self.token, self.username)


# 附带功能
def Doki2(token: str) -> Tuple[bool, JpaUsers]:
    Token_list = JpaTokens.objects.filter(token=token).filter(expire_time__gte=datetime.now())
    if len(Token_list) != 1:
        return False, None
    Token = Token_list[0]
    Token.expire_time = Token.expire_time + timedelta(minutes=15)
    Token.save()
    username = Token.username
    try:
        user = JpaUsers.objects.get(username=username)
    except Exception:
        return False, None
    return True, user
