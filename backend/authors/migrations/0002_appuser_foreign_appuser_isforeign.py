# Generated by Django 4.2.6 on 2023-12-03 04:48

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='foreign',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name='appuser',
            name='isForeign',
            field=models.BooleanField(default=False),
        ),
    ]
