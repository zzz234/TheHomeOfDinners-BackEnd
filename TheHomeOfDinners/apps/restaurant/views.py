from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.models import User
from .models import Restaurant
from rest_framework.response import Response

from restaurant.serializers import RestaurantSerializer


class RestaurantView(CreateAPIView):
    serializer_class = RestaurantSerializer


class RestaurantModelViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    # def get(self, request, pk):
    #     try:
    #         restaurant = Restaurant.objects.get(pk=pk)
    #     except Exception:
    #         return Response({'message': '找不到数据!'})
    #     serializer = RestaurantSerializer(instance=restaurant)
    #     return Response(serializer.data)
