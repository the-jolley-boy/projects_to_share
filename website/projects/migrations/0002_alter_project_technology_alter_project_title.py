# Generated by Django 4.1.7 on 2023-04-20 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='technology',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
