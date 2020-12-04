from django.db import models


class Restaurant(models.Model):
    res_name = models.CharField(max_length=20, unique=True, verbose_name='餐馆名称')
    owner = models.IntegerField(verbose_name='餐馆创建者')
    res_address = models.CharField(max_length=200, unique=True, verbose_name='餐馆地址')
    picture = models.CharField(max_length=400, verbose_name='餐馆封面图片')
    score = models.FloatField(verbose_name='餐馆评分')
    business_time = models.CharField(max_length=100, verbose_name='营业时间')
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    verify = models.CharField(max_length=1, verbose_name='审核状态(0-审核中，1-审核通过，-1-审核未通过)')

    class Meta:
        db_table = 'tb_restaurant'
        verbose_name = '餐馆'
        verbose_name_plural = verbose_name


class Menu(models.Model):
    restaurant = models.IntegerField(verbose_name='所属餐馆')
    name = models.CharField(max_length=20, verbose_name='菜品名称')
    picture = models.CharField(max_length=400, verbose_name='菜品封面图片')
    recommendations = models.IntegerField(verbose_name='推荐数')
    price = models.FloatField(verbose_name='单价')

    class Meta:
        db_table = 'tb_menu'
        verbose_name = '菜单'
        verbose_name_plural = verbose_name


class Review(models.Model):
    user = models.IntegerField(verbose_name='所属用户')
    restaurant = models.IntegerField(verbose_name='所属餐馆')
    datetime = models.DateTimeField(verbose_name='评论时间')
    text = models.CharField(max_length=1000, verbose_name='评论内容')
    score = models.FloatField(verbose_name='餐馆评分')
    depend = models.IntegerField(default=-1, verbose_name='从属评论')

    class Meta:
        db_table = 'tb_review'
        verbose_name = '评论'
        verbose_name_plural = verbose_name


class Collection(models.Model):
    user = models.IntegerField(verbose_name='所属用户')
    restaurant = models.IntegerField(verbose_name='所属餐馆')
    datetime = models.DateTimeField(verbose_name='评论时间')

    class Meta:
        db_table = 'tb_collection'
        verbose_name = '收藏'
        verbose_name_plural = verbose_name


class Pictures(models.Model):
    FLAGS = (
        (1, '餐馆图片'),
        (2, '菜单图片'),
        (3, '评论图片'),
    )
    picture = models.CharField(max_length=400, verbose_name='餐馆封面图片')

    class Meta:
        db_table = 'tb_pictures'
        verbose_name = '收藏'
        verbose_name_plural = verbose_name
