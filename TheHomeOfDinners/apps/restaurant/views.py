import json
import os

from django.db.models import Q, F, Avg, Count
from rest_framework import status
# Create your views here.
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

import parameters
from restaurant.serializers import RestaurantSerializer, CollectionSerializer, MenuSerializer, ReviewSerializer
from .models import Restaurant, Tag, Collection, Menu, Review
from .utils import MyPageNumberPagination


class RestaurantModelViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    pagination_class = MyPageNumberPagination

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        try:
            # 删除之前的图片
            os.remove(instance.picture.path)
        except Exception:
            pass

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def reviews_count(self, request, pk):
        counts = Review.objects.filter(restaurant=pk) \
            .values('score') \
            .annotate(count=Count('score')) \
            .values_list('score', 'count')
        res = {}
        for count in counts:
            res[count[0]] = count[1]
        return Response(res)


class TagRestaurantDetailView(GenericAPIView):
    serializer_class = RestaurantSerializer
    pagination_class = MyPageNumberPagination

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
        # 对返回结果进行处理
        restaurant = self.paginate_queryset(restaurant)  # 获取分页数据
        serializer = self.get_serializer(restaurant, many=True)
        return self.get_paginated_response(serializer.data)  # 返回分页类型


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
    pagination_class = MyPageNumberPagination

    @action(methods=['post'], detail=False)
    def del_by_user_restaurant(self, request):
        """
        取消收藏
        :param request: 'user','restaurant'
        """
        user = request.data['user']
        restaurant = request.data['restaurant']
        collection = Collection.objects.get(Q(user=user) & Q(restaurant=restaurant))
        collection.delete()
        return Response("删除成功!")

    @action(methods=['get'], detail=True)
    def collection_count(self, request, pk):
        """获取餐馆被收藏的数目"""
        count = Collection.objects.filter(restaurant=pk).count()
        return Response(count)

    @action(methods=['get'], detail=True)
    def restaurant(self, request, pk):
        """获取收藏的餐馆列表"""
        restaurants = Restaurant.objects.filter(restaurant_collection__user_id=pk)
        restaurants = self.paginate_queryset(restaurants)
        serializer = RestaurantSerializer(instance=restaurants, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['post'], detail=False)
    def collected(self, request):
        """检查是否收藏"""
        user, restaurant = request.data['user'], request.data['restaurant']
        count = Collection.objects.filter(Q(user=user) & Q(restaurant=restaurant)).count()
        return Response(count)


class MenuModelViewSet(ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    pagination_class = MyPageNumberPagination

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        try:
            # 删除之前的图片
            os.remove(instance.picture.path)
        except Exception:
            pass

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def restaurant_menu(self, request, pk):
        """根据餐馆id获取菜单列表"""
        menu = Menu.objects.filter(restaurant=pk).order_by('-recommendations')
        menu = self.paginate_queryset(menu)
        serializer = self.get_serializer(menu, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['post'], detail=False)
    def res_insert(self, request):
        """测试用的接口，不要调用"""
        request.data['name'] = str(request.data['picture']).split('.')[0]
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['post'], detail=False)
    def recommended(self, request):
        """
        为指定菜品添加一个推荐数
        post的body中携带参数menus，格式为[1,2,3,4]
        """
        menus = json.loads(request.data['menus'])
        count = Menu.objects.filter(id__in=menus).update(recommendations=F('recommendations') + 1)
        return Response(count)


class ReviewModelViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = MyPageNumberPagination

    @action(methods=['get'], detail=True)
    def restaurant_review(self, request, pk):
        reviews = Review.objects.filter(restaurant=pk)
        reviews = self.paginate_queryset(reviews)
        serializer = self.get_serializer(reviews, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        restaurant = request.data['restaurant']
        score = Review.objects.filter(restaurant=restaurant).values('restaurant').annotate(
            avg_score=Avg('score')).values_list(
            'avg_score')[0][0]
        Restaurant.objects.filter(id=restaurant).update(score=score)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
