# Generated by Django 4.2.6 on 2023-10-27 02:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_alter_post_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
    ]
