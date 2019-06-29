# Generated by Django 2.2.2 on 2019-06-28 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='comments_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='likes_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]