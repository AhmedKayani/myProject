# Generated by Django 3.2 on 2024-05-29 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crudApp', '0002_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crud',
            name='networth',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
    ]
