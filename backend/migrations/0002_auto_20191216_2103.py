# Generated by Django 3.0 on 2019-12-16 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='schedules',
            field=models.ManyToManyField(null=True, related_name='sitters_concerned', to='backend.Schedule'),
        ),
    ]
