import os

from django.db.models import Q
# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

import parameters
from restaurant.serializers import RestaurantSerializer, CollectionSerializer
from .models import Restaurant, Tag, Collection
from .utils import MyPageNumberPagination


class RestaurantModelViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    pagination_class = MyPageNumberPagination

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # 删除之前的图片
        os.remove(instance.picture.path)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class TagRestaurantDetailView(APIView):

    def get(self, request, param):
        """根据标签查询餐馆"""

        # 解析参数
        param1, param2 = None, None
        if 'c' in param:
            if 'l' in param:
                il = param.find('l')
                param1, param2 = param[1:il], param[il + 1:]
            else:
                param1 = param[1:]
        else:
            if 'l' in param:
                param1 = param[1:]
        restaurant = None
        # 根据参数进行查询
        if param1:
            restaurant = Restaurant.objects.filter(tag__tag_name=param1)
        if param2:
            restaurant = restaurant.filter(tag__tag_name=param2)
        pagination = MyPageNumberPagination()  # 分页器
        restaurant = pagination.paginate_queryset(restaurant, request, self)  # 获取分页数据
        serializer = RestaurantSerializer(instance=restaurant, many=True)  # 序列化
        return pagination.get_paginated_response(serializer.data)  # 返回分页类型


class TagDetailView(APIView):
    def get(self, request):
        """获取标签数据"""
        if parameters.Tags:
            # 如果已经有缓存，则直接读取缓存
            return Response(parameters.Tags)
        # 获取标签种类
        tag_types = Tag.objects.values_list('tag_type').distinct()
        res = {}
        for tag_type in tag_types:
            res[Tag.objects.filter(tag_type=tag_type[0]).first().get_tag_type_display()] = []
        # 获取标签数据
        tags = Tag.objects.values_list('tag_type', 'tag_name')
        # 将标签数据进行分类
        for tag in tags:
            res[Tag.objects.filter(tag_type=tag[0]).first().get_tag_type_display()].append(tag[1])
        parameters.Tags = res
        return Response(res)

    def delete(self, request):
        parameters.Tags = None
        return Response("缓存清除成功！")


class CollectionModelViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    @action(methods=['get'], detail=True)
    def collection_count(self, request, pk):
        """获取餐馆被收藏的数目"""
        count = Collection.objects.filter(restaurant=pk).count()
        return Response(count)

    @action(methods=['get'], detail=True)
    def restaurant(self, request, pk):
        """获取收藏的餐馆列表"""
        restaurants = Restaurant.objects.filter(restaurant_collection__user_id=pk)
        serializer = RestaurantSerializer(instance=restaurants, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def collected(self, request):
        """检查是否收藏"""
        user, restaurant = request.data['user'], request.data['restaurant']
        count = Collection.objects.filter(Q(user=user) & Q(restaurant=restaurant)).count()
        return Response(count)
