# Generated by Django 3.1.2 on 2020-12-27 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0013_auto_20201227_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='depend',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurant.review', verbose_name='所属评论'),
        ),
    ]
