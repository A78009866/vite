# Generated by Django 5.1.6 on 2025-05-30 08:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vite', '0009_customuser_qr_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_url', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('color1', models.CharField(default='#4FACFE', max_length=7)),
                ('color2', models.CharField(default='#00F2FE', max_length=7)),
                ('is_video', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Stories',
                'ordering': ['-created_at'],
            },
        ),
    ]
