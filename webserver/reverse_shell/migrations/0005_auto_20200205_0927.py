# Generated by Django 3.0.2 on 2020-02-05 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reverse_shell', '0004_auto_20200205_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attacker',
            name='mac_address',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='victim',
            name='mac_address',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]