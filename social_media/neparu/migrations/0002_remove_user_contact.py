# Generated by Django 2.2.4 on 2020-03-16 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neparu', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='contact',
        ),
    ]