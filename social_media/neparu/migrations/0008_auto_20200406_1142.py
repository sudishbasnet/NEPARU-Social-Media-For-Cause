# Generated by Django 2.2.4 on 2020-04-06 05:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neparu', '0007_auto_20200405_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inbox',
            name='feedback_receiver',
            field=models.ManyToManyField(blank=True, related_name='feedback_receiver', to=settings.AUTH_USER_MODEL),
        ),
    ]
