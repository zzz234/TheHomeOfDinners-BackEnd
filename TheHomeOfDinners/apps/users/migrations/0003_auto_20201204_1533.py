# Generated by Django 3.1.2 on 2020-12-04 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.CharField(max_length=400, verbose_name='用户头像'),
        ),
    ]
