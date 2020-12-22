import re

from rest_framework import serializers

from restaurant.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    """餐馆序列化器"""

    # ['res_name','owner','res_address','picture','score','business_time','mobile','verify']
    class Meta:
        model = Restaurant
        fields = '__all__'
        # fields = ['id', 'res_name', 'owner', 'res_address', 'picture', 'score', 'business_time', 'mobile', 'verify']
        # read_only_fields = ['verify']

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
