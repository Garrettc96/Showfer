# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_anime_arg'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anime',
            name='image',
        ),
    ]
