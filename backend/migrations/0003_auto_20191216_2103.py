# Generated by Django 3.0 on 2019-12-16 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20191216_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='schedules',
            field=models.ManyToManyField(blank=True, null=True, related_name='sitters_concerned', to='backend.Schedule'),
        ),
    ]
