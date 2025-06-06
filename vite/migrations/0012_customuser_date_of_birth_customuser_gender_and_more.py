# Generated by Django 5.1.6 on 2025-06-04 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vite', '0011_delete_story'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'ذكر'), ('female', 'أنثى'), ('other', 'آخر'), ('', 'أفضل عدم القول')], default='', max_length=10),
        ),
        migrations.AddField(
            model_name='customuser',
            name='relationship_status',
            field=models.CharField(blank=True, choices=[('single', 'أعزب/عزباء'), ('in_relationship', 'في علاقة'), ('engaged', 'مخطوب/مخطوبة'), ('married', 'متزوج/متزوجة'), ('complicated', 'معقد'), ('open_relationship', 'علاقة مفتوحة'), ('', 'أفضل عدم القول')], default='', max_length=20),
        ),
    ]
