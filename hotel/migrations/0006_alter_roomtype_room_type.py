# Generated by Django 4.0.4 on 2022-07-04 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0005_roomtype_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomtype',
            name='room_type',
            field=models.CharField(choices=[('single', 'single'), ('double', 'double'), ('premium', 'premium')], default='single', max_length=9),
        ),
    ]