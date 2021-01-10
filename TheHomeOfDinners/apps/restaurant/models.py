from django.db import models

from users.models import User


class Restaurant(models.Model):
    VERIFY = (
        ('0', '审核中'),
        ('1', '审核通过'),
        ('2', '审核未通过'),
    )
    res_name = models.CharField(max_length=40, unique=True, verbose_name='餐馆名称')
    # 设置创建者外键，当创建者注销时，餐馆也被注销
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='餐馆创建者', related_name='restaurant')
    res_address = models.CharField(max_length=200, unique=True, verbose_name='餐馆地址')
    picture = models.ImageField(upload_to='restaurant', null=True, blank=True, verbose_name='餐馆封面图片')
    score = models.FloatField(verbose_name='餐馆评分', default=0)
    business_time = models.CharField(max_length=100, verbose_name='营业时间', null=True)
    mobile = models.CharField(max_length=11, unique=True, verbose_name='联系方式')
    verify = models.CharField(max_length=2, choices=VERIFY, verbose_name='审核状态(0-审核中，1-审核通过，2-审核未通过)', default='0')

    class Meta:
        db_table = 'tb_restaurant'
        verbose_name = '餐馆'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.res_name


class Menu(models.Model):
    # 设置所属餐馆外键，当餐馆注销时，菜单也被注销
    restaurant = models.ForeignKey(to=Restaurant, on_delete=models.CASCADE, verbose_name='所属餐馆',
                                   related_name='menu')
    name = models.CharField(max_length=20, verbose_name='菜品名称')
    picture = models.ImageField(upload_to='menu', null=True, blank=True, verbose_name='菜品封面图片')
    recommendations = models.IntegerField(verbose_name='推荐数', default=0)
    price = models.FloatField(verbose_name='单价', default=0.0)

    class Meta:
        db_table = 'tb_menu'
        verbose_name = '菜单'
        verbose_name_plural = verbose_name
        unique_together = ["restaurant", "name", ]
        index_together = ["restaurant", "name", ]

    def __str__(self):
        return self.restaurant.res_name + ' ' + self.name


class Review(models.Model):
    # 设置发布评论者外键，当用户注销时，评论仍被保留
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, verbose_name='评论发布者',
                             related_name='user_review')
    # 设置所属餐馆外键，当餐馆注销时，评论也被注销
    restaurant = models.ForeignKey(to=Restaurant, on_delete=models.CASCADE, verbose_name='所属餐馆',
                                   related_name='restaurant_review')
    datetime = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)
    text = models.CharField(max_length=1000, verbose_name='评论内容')
    score = models.IntegerField(verbose_name='餐馆评分')
    depend = models.ForeignKey(to='self', blank=True, null=True, on_delete=models.CASCADE, verbose_name='所属评论')

    class Meta:
        db_table = 'tb_review'
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.get_username() + ' ' + self.restaurant.res_name


class Collection(models.Model):
    # 设置用户外键，当用户注销时，收藏被删除
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='评论发布者', related_name='user_collection')
    # 设置餐馆外键，当餐馆注销时，收藏被保留
    restaurant = models.ForeignKey(to=Restaurant, on_delete=models.SET_NULL, null=True, verbose_name='所属餐馆',
                                   related_name='restaurant_collection')
    datetime = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)

    class Meta:
        db_table = 'tb_collection'
        verbose_name = '收藏'
        verbose_name_plural = verbose_name
        unique_together = ["user", "restaurant"]
        index_together = ["user", "restaurant"]


class Pictures(models.Model):
    OWNER = (
        ('1', '餐馆图片'),
        ('2', '菜单图片'),
        ('3', '评论图片'),
    )
    owner_type = models.CharField(max_length=1, choices=OWNER, verbose_name='图片所属者')
    owner_id = models.IntegerField(verbose_name='图片所属者ID')
    picture = models.CharField(max_length=400, verbose_name='餐馆封面图片')

    class Meta:
        db_table = 'tb_pictures'
        verbose_name = '收藏'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    TAG_TYPE = (
        (1, '种类'),
        (2, '地区'),
    )
    restaurant = models.ManyToManyField(Restaurant, verbose_name='对应餐馆', related_name='tag')
    tag_type = models.IntegerField(choices=TAG_TYPE, verbose_name='标签种类')
    tag_name = models.CharField(max_length=20, verbose_name='标签名')

    class Meta:
        db_table = 'tb_tag'
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag_name