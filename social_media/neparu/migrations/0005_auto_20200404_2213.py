# Generated by Django 2.2.4 on 2020-04-04 16:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('neparu', '0004_auto_20200404_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='inbox',
            name='feedback_receiver',
            field=models.ManyToManyField(blank=True, null=True, related_name='feedback_receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='inbox',
            name='receiver',
        ),
        migrations.AddField(
            model_name='inbox',
            name='receiver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL),
        ),
    ]
