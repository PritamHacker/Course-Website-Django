# Generated by Django 4.2.4 on 2023-08-17 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courseapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordereditem',
            name='quantity',
        ),
    ]
