# Generated by Django 4.0.4 on 2022-07-04 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='room_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.roomtype'),
        ),
    ]
