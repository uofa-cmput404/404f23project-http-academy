# Generated by Django 4.2.7 on 2023-12-09 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_alter_post_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image_url',
            field=models.URLField(max_length=500, null=True),
        ),
    ]
