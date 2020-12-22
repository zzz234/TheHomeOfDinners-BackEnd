from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    """自定义用户模型类，需在配置文件中重新指定默认用户模型类"""
    ROLE = (
        ('0', '管理员'),
        ('1', '用户'),
        ('2', '商家'),
    )
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    picture = models.CharField(max_length=400, verbose_name='用户头像')
    role = models.CharField(max_length=1, choices=ROLE, verbose_name='角色(0-管理员，1-用户，2、商家)')
    introduction = models.CharField(max_length=400, verbose_name='个人简介')

    class Meta:  # 配置数据库表名
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
