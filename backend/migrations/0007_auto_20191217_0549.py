# Generated by Django 3.0 on 2019-12-17 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_auto_20191217_0536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avgMark',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=2),
        ),
    ]
