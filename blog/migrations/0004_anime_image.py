# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_remove_anime_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='anime',
            name='image',
            field=models.ImageField(null=True, upload_to=b'blog/media'),
        ),
    ]
