# Generated by Django 4.2.6 on 2023-10-26 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_alter_post_caption'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.TextField(max_length=500, null=True),
        ),
    ]