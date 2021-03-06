# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-09-06 16:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0009_auto_20170822_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membertype',
            name='begin_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='membertype',
            name='type',
            field=models.CharField(choices=[('PH', 'Phux'), ('OM', 'Ordinarie Medlem'), ('JS', 'JuniorStÄlM'), ('ST', 'StÄlM'), ('FG', 'Färdig'), ('EM', 'Ej längre medlem'), ('VP', 'Viktig person'), ('KA', 'Kanslist'), ('IM', 'Inte medlem'), ('KE', 'Kanslist emerita')], default='PH', max_length=2),
        ),
    ]
