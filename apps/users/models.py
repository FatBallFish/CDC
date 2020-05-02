from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime


# Create your models here.
# class JpaUsers_bak(models.Model):
#     username = models.CharField(verbose_name="用户名", primary_key=True, max_length=20)
#     nickname = models.CharField(verbose_name="昵称", max_length=20, blank=True, null=True)
#     password = models.CharField(verbose_name="密码", max_length=100)
#     age = models.CharField(verbose_name="年龄", max_length=3, blank=True, null=True)
#     real_auth_id = models.CharField(verbose_name="实名信息id", max_length=18, blank=True, null=True)
#     email = models.CharField(verbose_name="邮箱", max_length=30, blank=True, null=True)
#     phone = models.CharField(verbose_name="手机号", max_length=11)
#     image = models.ImageField(verbose_name="头像", blank=True, null=True)
#     salt = models.CharField(verbose_name="盐", max_length=30, blank=True, null=True)
#     create_time = models.DateTimeField(verbose_name="创建时间", blank=True, null=True)
#     last_modified_time = models.DateTimeField(verbose_name="最后登录时间")
#     is_active = models.CharField(verbose_name="是否有效", max_length=1, blank=True, null=True)
#
#     class Meta:
#         verbose_name = "用户"
#         verbose_name_plural = verbose_name
#         managed = False
#         db_table = 'jpa_users'
#         abstract = True
#
#     def __str__(self):
#         return "{}".format(self.username)

class MyMgr(BaseUserManager):
    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class JpaUsers(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name="用户名", primary_key=True, max_length=20, unique=True)
    nickname = models.CharField(verbose_name="昵称", max_length=20, blank=True, null=True)
    age = models.CharField(verbose_name="年龄", max_length=3, blank=True, null=True)
    real_auth_id = models.CharField(verbose_name="实名信息id", max_length=18, blank=True, null=True)
    email = models.CharField(verbose_name="邮箱", max_length=30, blank=True, null=True)
    phone = models.CharField(verbose_name="手机号", max_length=11, null=True)
    image = models.ImageField(verbose_name="头像", blank=True, null=True)
    salt = models.CharField(verbose_name="盐", max_length=30, blank=True, null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", default=datetime.now)
    last_modified_time = models.DateTimeField(verbose_name="最后登录时间", null=True)
    is_active = models.BooleanField(verbose_name="是否有效", default=True, blank=True, null=True)
    gender = models.CharField(verbose_name="性别", max_length=5, null=True, blank=True)
    user_group = models.CharField(verbose_name="用户身份", max_length=50, default="NORMAL")
    is_staff = models.BooleanField(verbose_name="是否是员工", default=False)
    is_superuser = models.BooleanField(verbose_name="是否是超级管理员", default=False)
    USERNAME_FIELD = "username"
    objects = MyMgr()

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        # managed = False
        db_table = 'jpa_users'

    def __str__(self):
        return "{}".format(self.username)

    def clean(self):
        super().clean()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.nickname
