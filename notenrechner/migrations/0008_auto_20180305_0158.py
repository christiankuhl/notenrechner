# Generated by Django 2.0.2 on 2018-03-05 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notenrechner', '0007_auto_20180305_0157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aufgabenabgabe',
            name='punkte',
            field=models.DecimalField(decimal_places=1, max_digits=4, null=True),
        ),
    ]
