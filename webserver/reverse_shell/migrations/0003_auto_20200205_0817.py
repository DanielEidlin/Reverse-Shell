# Generated by Django 3.0.2 on 2020-02-05 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reverse_shell', '0002_auto_20200124_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attacker',
            name='computer_name',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='victim',
            name='computer_name',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]