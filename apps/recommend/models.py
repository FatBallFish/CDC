from django.db import models

from datetime import datetime


# Create your models here.
class JpaStores(models.Model):
    is_active_status = ((0, "打烊"), (1, "营业中"), (2, "违规冻结"), (3, "临时关店"), (4, "永久封店"), (5, "已注销"))

    id = models.CharField(verbose_name="店铺id", primary_key=True, max_length=30)
    name = models.CharField(verbose_name="店铺名称", max_length=20, blank=True, null=True)
    owner_name = models.CharField(verbose_name="店家", max_length=20)
    store_index = models.TextField(verbose_name="店铺首页", blank=True, null=True)
    des = models.CharField(verbose_name="店铺简介", max_length=200, blank=True, null=True)
    tag = models.TextField(verbose_name="店铺标签", max_length=40, blank=True, null=True)
    district = models.CharField(verbose_name="省市区", max_length=100, blank=True, null=True)
    address = models.TextField(verbose_name="详细地址", blank=True, null=True)
    is_active = models.IntegerField(verbose_name="店铺状态", choices=is_active_status, blank=True, null=True)
    portrait = models.TextField(verbose_name="店铺图片", blank=True, null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", blank=True, null=True)
    lastmodified_time = models.DateTimeField(verbose_name="最后操作时间",
                                             db_column='lastModified_time')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'jpa_stores'
        verbose_name = "店铺"
        verbose_name_plural = verbose_name

    def delete(self, using=None, keep_parents=False):
        self.is_active = 5
        self.save()


class JpaItems(models.Model):
    item_status_choice = ((-1, "信息未完善"), (0, "未上架"), (1, "售卖中"), (2, "已下架"), (3, "已删除"))

    id = models.CharField(verbose_name="商品id", primary_key=True, max_length=10)
    item_name = models.TextField(verbose_name="商品名称", blank=True, null=True)
    store_id = models.CharField(verbose_name="店铺id", max_length=30, blank=True, null=True)
    item_type = models.CharField(verbose_name="商品类型", max_length=20, blank=True, null=True)
    item_des = models.TextField(verbose_name="商品详情", blank=True, null=True)
    item_portrait = models.TextField(verbose_name="商品图片", blank=True, null=True)
    item_status = models.IntegerField(verbose_name="商品状态", choices=item_status_choice, blank=True, null=True)
    original_price = models.DecimalField(verbose_name="商品原价格", max_digits=10, decimal_places=0, blank=True, null=True)
    discount_price = models.DecimalField(verbose_name="打折后价格", max_digits=10, decimal_places=0, blank=True, null=True)
    item_stock = models.IntegerField(verbose_name="库存量", blank=True, null=True)
    item_geohash = models.TextField(verbose_name="地理位置", blank=True, null=True)
    create_time = models.DateTimeField(verbose_name="创建时间")
    lastmodified_time = models.DateTimeField(verbose_name="最新操作时间",
                                             db_column='lastModified_time')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'jpa_items'
        verbose_name = "商品"
        verbose_name_plural = verbose_name


class JpaItemUserBehavior(models.Model):
    choice_behavior_type = ((1, "浏览"), (2, "收藏"), (3, "加入购物车"), (4, "购买"))

    username = models.CharField(verbose_name="用户id", max_length=20)
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
