# Generated by Django 3.1.2 on 2020-10-18 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcode',
            name='postcode',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]