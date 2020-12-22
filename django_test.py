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
    Test2()


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
    from restaurant.models import Tag,Restaurant
    restaurant = Restaurant.objects.get(pk=45).Tag.all()
    print(restaurant)

if __name__ == '__main__':
    main()
