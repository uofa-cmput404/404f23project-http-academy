# Generated by Django 4.2.6 on 2023-11-07 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0003_appuser_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='github',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appuser',
            name='host',
            field=models.URLField(max_length=2048, null=True),
        ),
        migrations.AddField(
            model_name='appuser',
            name='profileImage',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appuser',
            name='type',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='appuser',
            name='url',
            field=models.URLField(max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='username',
            field=models.CharField(max_length=140, null=True),
        ),
    ]