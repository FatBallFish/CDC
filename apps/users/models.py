from abc import ABC

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.html import format_html
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from CDC import settings
from extra_apps.m_cos import py_cos_main as COS
from extra_apps import MD5

from datetime import datetime

from apps.realauth.models import RealAuth
from apps.faces.models import FaceData


class BaseModel(models.Model):
    add_time = models.DateTimeField(verbose_name="创建时间", default=datetime.now)
    update_time = models.DateTimeField(verbose_name="更新时间", default=datetime.now)

    class Meta:
        abstract = True


# Create your models here.

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


@deconstructible
class CosStorage(Storage, ABC):
    path = ""

    def __init__(self, path: str = ""):
        self.path = path + "/"

    def save(self, name, content, max_length=None):
        suffix = name.split('.')[-1]
        img_data = content.read()
        print(img_data)
        key = self.path + MD5.md5_bytes(img_data) + ".user"
        print("key", key)
        # print(os.path.join(settings.BASE_DIR,"Program","NIAECv2",settings.MEDIA_URL,key))
        # with open(os.path.join(settings.BASE_DIR,"Program","NIAECv2",settings.MEDIA_URL,key),"wb") as f:
        #     f.write(img_data)
        try:
            COS.bytes_upload(body=img_data, key=key)
        except Exception as e:
            raise
        return settings.COS_ROOTURL + key

    def delete(self, name):
        print("delete:", name)
        # try:
        #     COS.delete_object()

    def url(self, name):
        # print("url:", name)
        return name


class JpaUsers(AbstractBaseUser, PermissionsMixin):
    gender_choice = (("男", "男"), ("女", "女"))

    username = models.CharField(verbose_name="用户名", primary_key=True, max_length=20, unique=True)
    nickname = models.CharField(verbose_name="昵称", max_length=20, blank=True, null=True)
    age = models.CharField(verbose_name="年龄", max_length=3, blank=True, null=True)
    real_auth = models.ForeignKey(verbose_name="实名认证信息", to=RealAuth, on_delete=models.SET_NULL, null=True,
                                  blank=True)
    email = models.CharField(verbose_name="邮箱", max_length=30, blank=True, null=True)
    phone = models.CharField(verbose_name="手机号", max_length=11, null=True)
    image = models.ImageField(verbose_name="头像", storage=CosStorage("/user/portrait"), blank=True, null=True,
                              max_length=1024)
    salt = models.CharField(verbose_name="盐", max_length=30, blank=True, null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", default=datetime.now)
    is_active = models.BooleanField(verbose_name="是否有效", default=True, blank=True, null=True)
    gender = models.CharField(verbose_name="性别", max_length=5, choices=gender_choice, null=True, blank=True)
    is_staff = models.BooleanField(verbose_name="是否是员工", default=False)
    is_superuser = models.BooleanField(verbose_name="是否是超级管理员", default=False)
    face = models.ForeignKey(verbose_name="人脸数据", to=FaceData, on_delete=models.SET_NULL, blank=True, null=True)

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

    def getImage(self):
        return format_html('<img src="{}" style="width:50px;height:auto">', self.image)

    getImage.short_description = "用户头像"
