#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TheHomeOfDinners.settings')
    import django
    django.setup()

    # Test1()
    # Test2()
    # Test3()
    # Test4()
    # Test5()
    # Test6()
    # Test7()
    Test8()


def Test1():
    # from users.models import User
    # print(User.objects.all())
    from restaurant.models import Tag
    tag7 = Tag.objects.get(tag_name='五一广场')
    tag8 = Tag.objects.get(tag_name='四方坪')
    tag9 = Tag.objects.get(tag_name='解放路')
    tag11 = Tag.objects.get(tag_name='坡子街')
    tag12 = Tag.objects.get(tag_name='其他')
    # 五一广场
    l7 = [9, 22, 26, 29, 30, 40, 41, 42, 45, 53, 55, 58, 59, 60, 61, 62, ]
    # 四方坪
    l8 = [12, 15, 20, 23, 32, 35, 38, 43, 48, 49, 50, ]
    # 解放路
    l9 = [11, 16, 21, 24, 25, 28, 33, 34, 44, 54, 57, ]
    # 坡子街
    l11 = [8, 10, 14, 17, 27, 36, 37, 46, 51, 56, ]
    # 其他
    l12 = [6, 13, 18, 19, 31, 39, 47, 52, ]
    tag7.restaurant.set(l7)
    tag8.restaurant.set(l8)
    tag9.restaurant.set(l9)
    tag11.restaurant.set(l11)
    tag12.restaurant.set(l12)
    # tag.restaurant.add(8)


def Test2():
    from restaurant.models import Tag, Restaurant
    params = ['小吃', '四方坪']
    restaurant = Restaurant.objects.filter(tag__tag_name=params[0]).filter(tag__tag_name=params[1])
    print(restaurant.count())
    # from restaurant.serializers import RestaurantSerializer
    # serializer = RestaurantSerializer(instance=restaurant, many=True)
    # print(serializer.data)


def Test3():
    from restaurant.models import Tag
    tag_types = Tag.objects.values_list('tag_type').distinct()
    res = {}
    for tag_type in tag_types:
        res[Tag.objects.filter(tag_type=tag_type[0]).first().get_tag_type_display()] = []
    print(res)
    tags = Tag.objects.values_list('tag_type', 'tag_name')
    for tag in tags:
        res[Tag.objects.filter(tag_type=tag[0]).first().get_tag_type_display()].append(tag[1])
    print(tags)


def Test4():
    from users.models import User

    from restaurant.models import Restaurant
    from restaurant.models import Collection
    # restaurants = Collection.objects.filter(user=6).values_list('restaurant')
    restaurant = Restaurant.objects.filter(restaurant_collection__user_id=2)
    print(restaurant)


def Test5():
    from users.models import User
    user = User.objects.get(pk=8)
    user.set_password('123456789')
    user.save()


def Test6():
    from restaurant.models import Restaurant
    restaurants = Restaurant.objects.all()


def Test7():
    from restaurant.models import Review
    from django.db.models import Avg, Count
    score = Review.objects.filter(restaurant=6).values('restaurant').annotate(avg_score=Avg('score')).values_list(
        'avg_score')[0][0]
    print(score)


def Test8():
    from restaurant.models import Review
    from django.db.models import Avg, Count
    counts = Review.objects.filter(restaurant=6).values('score').annotate(count=Count('score')).values_list('score',
                                                                                                      'count')
    res = {}
    for count in counts:
        res[count[0]] = count[1]
    print(res)


if __name__ == '__main__':
    main()
