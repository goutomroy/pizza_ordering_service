# Generated by Django 2.2.6 on 2019-11-02 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20191102_0929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'pending'), (2, 'cancelled'), (3, 'travelling'), (4, 'delivered')], default=1),
        ),
    ]