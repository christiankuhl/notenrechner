# Generated by Django 2.0.2 on 2018-03-04 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notenrechner', '0002_auto_20180304_1344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='klausur',
            name='anzahl_aufgaben',
        ),
    ]
