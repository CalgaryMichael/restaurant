# Generated by Django 2.2.1 on 2019-06-03 00:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0005_auto_20190602_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspection',
            name='inspection_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurant.InspectionType'),
        ),
        migrations.AlterField(
            model_name='inspection',
            name='score',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='restaurantcontact',
            name='phone',
            field=models.CharField(max_length=12, null=True),
        ),
    ]
