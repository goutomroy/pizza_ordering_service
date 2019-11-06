# Generated by Django 2.2.6 on 2019-11-03 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20191103_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Submitted'), (2, 'In Production'), (3, 'Travelling'), (4, 'Delivered'), (5, 'Cancelled')], default=1),
        ),
    ]
