# Generated by Django 2.2.4 on 2020-05-12 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neparu', '0009_auto_20200406_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='blood_group',
            field=models.CharField(blank=True, choices=[('', ''), ('AB+', 'AB+'), ('AB-', 'AB-'), ('A+', 'A+'), ('B+', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-')], max_length=2),
        ),
    ]
