# Generated by Django 5.1.6 on 2025-06-09 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vite', '0014_alter_notification_notification_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='last_active',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
