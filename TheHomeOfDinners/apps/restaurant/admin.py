from django.contrib import admin

# 管理员账号密码：
# 1admin（1是因为要校验身份）
# admin12345
# Register your models here.
from restaurant.models import Restaurant, Review, Tag, Menu


class TagAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'tag_type', 'tag_name', ]

    def restaurant(self, obj):
        return [r.res_name for r in obj.restaurant.all()]

    # 每页记录数
    list_per_page = 15


class RestaurantAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ('res_name', 'owner', 'res_address', 'picture', 'score',
                    'business_time', 'mobile', 'verify')

    list_filter = ('verify',)
    # 每页记录数
    list_per_page = 15
    # 查询字段
    search_fields = ('res_name',)


class ReviewAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ('user', 'restaurant', 'datetime', 'text', 'score', 'depend',)
    # list_filter = ('verify',)
    # 每页记录数
    list_per_page = 15
    # 查询字段
    # search_fields = ('res_name',)


class MenuAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ('restaurant', 'name', 'picture', 'recommendations', 'price',)
    # list_filter = ('verify',)
    # 每页记录数
    list_per_page = 15


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Menu, MenuAdmin)
