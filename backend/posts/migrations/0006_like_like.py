# Generated by Django 4.2.6 on 2023-11-11 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_remove_like_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='like',
            field=models.IntegerField(default=0),
        ),
    ]
