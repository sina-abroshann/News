# Generated by Django 4.1 on 2022-08-11 07:39

from django.db import migrations
import django.utils.timezone
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_comment_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='add_time_jalali',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
