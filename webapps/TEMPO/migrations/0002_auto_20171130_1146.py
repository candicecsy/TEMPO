# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-30 16:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TEMPO', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SongList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song_name', models.CharField(max_length=20)),
                ('music_score', models.FileField(upload_to='')),
            ],
        ),
        migrations.RemoveField(
            model_name='bandevent',
            name='song_list',
        ),
        migrations.AddField(
            model_name='songlist',
            name='band_event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TEMPO.BandEvent'),
        ),
    ]