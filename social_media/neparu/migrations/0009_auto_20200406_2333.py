# Generated by Django 2.2.4 on 2020-04-06 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neparu', '0008_auto_20200406_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
