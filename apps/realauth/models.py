from django.db import models


# Create your models here.
class JpaRealauth(models.Model):
    real_auth_id = models.CharField(primary_key=True, max_length=18)
    name = models.CharField(max_length=10, blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=30, blank=True, null=True)
    birthday = models.DateTimeField(blank=True, null=True)
    nation = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jpa_realauth'
        verbose_name = "实名认证"
        verbose_name_plural = verbose_name
