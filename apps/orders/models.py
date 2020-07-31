from django.db import models
from apps.products.models import JpaItems, JpaStores


# Create your models here.
class JpaOrderform(models.Model):
    pay_choice = ((0, "待支付"), (1, "已支付"), (2, "已取消"))
    transport_choice = ((0, "待派送"), (1, "派送中"), (2, "已送达"))

    serial_number = models.CharField(verbose_name="订单流水号", max_length=18)
    store = models.ForeignKey(verbose_name="店铺", to=JpaStores, on_delete=models.DO_NOTHING)
    # store_id = models.CharField(verbose_name="店铺id", max_length=30)
    item = models.ForeignKey(verbose_name="商品", to=JpaItems, on_delete=models.DO_NOTHING)
    # item_id = models.CharField(verbose_name="商品id", max_length=10)
    username = models.CharField(verbose_name="用户名", max_length=20)
    item_num = models.IntegerField(verbose_name="商品数量", blank=True, null=True)
    item_price = models.DecimalField(verbose_name="商品价格", max_digits=10, decimal_places=0, blank=True, null=True)
    real_price = models.DecimalField(verbose_name="实付金额", max_digits=10, decimal_places=0, blank=True, null=True)
    pay_status = models.IntegerField(verbose_name="支付状态", choices=pay_choice, blank=True, null=True)
    transport_status = models.IntegerField(verbose_name="配送状态", choices=transport_choice, blank=True, null=True)
    createtime = models.DateTimeField(verbose_name="创建时间", db_column='createTime')  # Field name made lowercase.
    cancle_time = models.DateTimeField(verbose_name="取消时间", blank=True, null=True)
    pay_time = models.DateTimeField(verbose_name="支付时间", blank=True, null=True)
    send_time = models.DateTimeField(verbose_name="出货时间", blank=True, null=True)
    refund_time = models.DateTimeField(verbose_name="退款时间", blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jpa_orderform'
        verbose_name = "订单列表"
        verbose_name_plural = verbose_name
