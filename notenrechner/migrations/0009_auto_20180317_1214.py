# Generated by Django 2.0.2 on 2018-03-17 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notenrechner', '0008_auto_20180305_0158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aufgabe',
            name='max_punkte',
            field=models.DecimalField(decimal_places=1, default=10, max_digits=4, null=True),
        ),
    ]
