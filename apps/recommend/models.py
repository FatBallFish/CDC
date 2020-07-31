from django.db import models

from apps.users.models import JpaUsers
from datetime import datetime

# Create your models here.
from django.utils.html import format_html


class JpaItemUserBehavior(models.Model):
    choice_behavior_type = ((1, "浏览"), (2, "收藏"), (3, "加入购物车"), (4, "购买"))

    username = models.CharField(verbose_name="用户id", max_length=20)
    # username = models.ForeignKey(verbose_name="用户id", to=JpaUsers, on_delete=models.CASCADE)
    item_id = models.CharField(verbose_name="商品id", max_length=10, blank=True, null=True)
    item_type = models.CharField(verbose_name="商品分类", max_length=100, blank=True, null=True)
    behavior_type = models.IntegerField(verbose_name="用户行为", choices=choice_behavior_type, blank=True, null=True)
    user_geohash = models.TextField(verbose_name="用户位置", blank=True, null=True)
    happen_time = models.DateTimeField(verbose_name="发生时间", blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jpa_item_user_behavior'
        verbose_name = "商品-用户行为"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}-{}".format(self.username, self.behavior_type)
