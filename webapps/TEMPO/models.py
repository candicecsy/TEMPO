# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date
from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from django.core.validators import MinValueValidator

# Create Band model
class Band(models.Model):
    band_name = models.CharField(max_length=100, primary_key=True, unique=True)
    band_description = models.TextField(max_length=500, blank=True)
    band_photo = models.ImageField(upload_to="band_photo", blank=True)

    @staticmethod
    def get_members(self):
        return Profile.objects.filter(band=self)

class BandEvent(models.Model):
    band = models.ForeignKey(Band, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    date_time = models.DateField(default=date.today)
    location = models.CharField(max_length=100)
    poster_photo = models.ImageField(upload_to="poster_photo")
    is_live = models.BooleanField(default=False)
    is_end = models.BooleanField(default=False)

class SongList(models.Model):
    band_event = models.ForeignKey(BandEvent, on_delete=models.CASCADE, null=True)
    song_name = models.CharField(max_length=20)
    music_score = models.FileField(upload_to="music_score")

# Create the one to one field with User
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birthday = models.DateField(null=True, blank=True)
    age = models.IntegerField(default=0, blank=True, validators=[MinValueValidator(0)])
    band = models.ForeignKey(Band, on_delete=models.CASCADE, default=None, null=True)
    picture = models.ImageField(upload_to="user_photo", blank=True, null=True)
    subscribe_events = models.ManyToManyField(BandEvent)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class PracticeSession(models.Model):
    band = models.ForeignKey(Band, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    date_time = models.DateField(default=date.today)
    is_live = models.BooleanField(default=False)
    is_end = models.BooleanField(default=False)
    starter = models.CharField(max_length=200, blank=True, null=True)
