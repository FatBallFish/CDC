from django.db import models


# Create your models here.
class JpaUsers(models.Model):
    username = models.CharField(verbose_name="用户名", primary_key=True, max_length=20)
    nickname = models.CharField(verbose_name="昵称", max_length=20, blank=True, null=True)
    password = models.CharField(verbose_name="密码", max_length=100)
    age = models.CharField(verbose_name="年龄", max_length=3, blank=True, null=True)
    real_auth_id = models.CharField(verbose_name="实名信息id", max_length=18, blank=True, null=True)
    email = models.CharField(verbose_name="邮箱", max_length=30, blank=True, null=True)
    phone = models.CharField(verbose_name="手机号", max_length=11)
    image = models.ImageField(verbose_name="头像", blank=True, null=True)
    salt = models.CharField(verbose_name="盐", max_length=30, blank=True, null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", blank=True, null=True)
    last_modified_time = models.DateTimeField(verbose_name="最后登录时间")
    is_active = models.CharField(verbose_name="是否有效", max_length=1, blank=True, null=True)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'jpa_users'

    def __str__(self):
        return "{}".format(self.username)
