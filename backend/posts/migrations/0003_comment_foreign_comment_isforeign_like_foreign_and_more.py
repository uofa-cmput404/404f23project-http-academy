# Generated by Django 4.2.6 on 2023-12-04 06:58

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_foreign_post_isforeign'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='foreign',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name='comment',
            name='isForeign',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='like',
            name='foreign',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name='like',
            name='isForeign',
            field=models.BooleanField(default=False),
        ),
    ]
