# Generated by Django 2.0.2 on 2018-02-23 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roomres', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='comment',
            field=models.TextField(null=True),
        ),
    ]
