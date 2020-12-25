import re

from rest_framework import serializers

from restaurant.models import Restaurant, Tag, Collection


class RestaurantSerializer(serializers.ModelSerializer):
    # 餐馆序列化器
    class Meta:
        model = Restaurant
        fields = '__all__'

    def validate_mobile(self, value):
        """单独校验手机号"""
        if not re.match(r'1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式有误')
        return value

    def create(self, validated_data):
        # 设置默认审核状态为未审核
        validated_data['verify'] = '0'
        restaurant = Restaurant(**validated_data)
        restaurant.save()
        return restaurant


class TagSerializer(serializers.ModelSerializer):
    # 标签序列化器
    class Meta:
        model = Tag
        fields = '__all__'


class CollectionSerializer(serializers.ModelSerializer):
    # 收藏序列化器
    class Meta:
        model = Collection
        fields = '__all__'
        read_only_fields = ['datetime']
