# Generated by Django 4.2.6 on 2023-10-30 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=100)),
                ('host', models.CharField(max_length=100)),
                ('displayName', models.CharField(max_length=100)),
                ('github', models.CharField(max_length=100)),
                ('profileImage', models.CharField(max_length=100)),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
    ]
