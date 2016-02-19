# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_anime_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='anime',
            name='year',
            field=models.TextField(default='None'),
            preserve_default=False,
        ),
    ]
