# Generated by Django 3.0.3 on 2020-03-01 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reverse_shell', '0011_auto_20200301_2235'),
    ]

    operations = [
        migrations.AddField(
            model_name='attacker',
            name='victim',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reverse_shell.Victim'),
        ),
    ]
