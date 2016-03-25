# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-22 03:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invitation', '0006_attendance_choices_are_now_not_required'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest',
            name='meal_choice',
            field=models.CharField(blank=True, choices=[(None, 'Reception Meal Choice'), ('veg', 'Vegetarian'), ('non-veg', 'Non-vegetarian (Fish and Chicken)')], max_length=7),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='invited_by',
            field=models.CharField(choices=[(None, 'Invited By'), ('verma', 'Verma Family'), ('gupta', 'Gupta Family')], max_length=5),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='name',
            field=models.SlugField(max_length=20, unique=True),
        ),
    ]