# Generated by Django 4.2.6 on 2023-11-19 22:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('followers', '0001_initial'),
        ('posts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Inbox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('authorId', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('follow_request', models.ManyToManyField(blank=True, to='followers.friendrequest')),
                ('like', models.ManyToManyField(blank=True, to='posts.like')),
                ('posts', models.ManyToManyField(blank=True, to='posts.post')),
            ],
        ),
    ]
