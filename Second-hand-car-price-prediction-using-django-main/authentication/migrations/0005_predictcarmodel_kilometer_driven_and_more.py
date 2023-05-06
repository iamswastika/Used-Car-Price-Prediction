# Generated by Django 4.1.7 on 2023-04-16 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0004_alter_predictcarmodel_fuel_type_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="predictcarmodel",
            name="kilometer_driven",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="predictcarmodel",
            name="seat",
            field=models.FloatField(default=0),
        ),
    ]
