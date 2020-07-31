from django.db import models
from apps.users.models import JpaUsers
from apps.products.models import JpaItems

from datetime import datetime


# Create your models here.
class Community(models.Model):
    sender = models.ForeignKey(verbose_name="发送者", to=JpaUsers, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="动态内容")
    item = models.ForeignKey(verbose_name="商品", to=JpaItems, on_delete=models.DO_NOTHING, null=True, blank=True)
    add_time = models.DateTimeField(verbose_name="创建时间", default=datetime.now)
    update_time = models.DateTimeField(verbose_name="更新时间", default=datetime.now)
    latitude = models.DecimalField(verbose_name="纬度", max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(verbose_name="经度", max_digits=10, decimal_places=7, blank=True, null=True)

    def __str__(self):
        return "{}({})".format(self.content, self.sender)

    class Meta:
        verbose_name = "社区动态"
        verbose_name_plural = verbose_name
        db_table = "communities"
