# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-29 09:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('certhelper', '0014_auto_20180718_1220'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='referencerun',
            options={'ordering': ('-reference_run', 'runtype', 'reco')},
        ),
        migrations.AlterModelOptions(
            name='type',
            options={'ordering': ('runtype', 'reco', 'bfield', 'beamtype', 'beamenergy', '-dataset')},
        ),
    ]