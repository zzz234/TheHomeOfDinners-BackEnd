# Generated by Django 3.1.2 on 2020-12-21 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20201204_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('0', '管理员'), ('1', '用户'), ('2', '商家')], max_length=1, verbose_name='角色(0-管理员，1-用户，2、商家)'),
        ),
    ]
