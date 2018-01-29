# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a User
from django.contrib.auth import login, authenticate
from django.db import transaction

from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404

from TEMPO.models import *
from TEMPO.forms import *

import json

# Helper function tp guess a MIME type from a file name
from mimetypes import guess_type


@login_required
def home(request):
    lives = BandEvent.objects.filter(is_live=True).filter(is_end=False)
    upcomings = BandEvent.objects.filter(is_live=False).filter(is_end=False)
    context = {'lives': lives, 'upcomings': upcomings}
    return render(request, 'TEMPO/user_home.html', context)


# the register function for registration
@transaction.atomic
def register(request):
    context = {}

    # Just display the registration form if this is a Get request
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'TEMPO/register.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'TEMPO/register.html', context)

    # If we get here the form data was valid, Register and login the user
    new_user = User.objects.create_user(username=form.cleaned_data.get('username'),
                                        password=form.cleaned_data.get('password1'),
                                        first_name=form.cleaned_data.get('first_name'),
                                        last_name=form.cleaned_data.get('last_name'),
                                        email=form.cleaned_data.get('email_address'))
    # new_user.is_active = False
    new_user.save()

    # Logs in the new user and redirects to his/her grumblr
    new_user = authenticate(username=form.cleaned_data.get('username'), \
                            password=form.cleaned_data.get('password1'))
    login(request, new_user)

    return redirect('/')


@login_required
def profile(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)

    if not profile.band:
        context = {'user': request.user, 'band': False}
    else:
        context = {'user': request.user, 'band': True}

    return render(request, 'TEMPO/profile.html', context)


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'GET':
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        context = {'user_form': user_form, 'profile_form': profile_form,
                   'id': request.user.id}
        return render(request, 'TEMPO/update_profile.html', context)

    user_form = UserForm(request.POST, instance=request.user)
    profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
    if not user_form.is_valid() or not profile_form.is_valid():
        context = {'user_form': user_form, 'profile_form': profile_form,
                   'id': request.user.id}
        return render(request, 'TEMPO/update_profile.html', context)

    user_form.save()
    profile_form.save()
    return redirect(reverse('profile'))


@login_required
@transaction.atomic
def create_band(request):
    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = BandForm()
        return render(request, 'TEMPO/create_band.html', context)

    form = BandForm(request.POST, request.FILES)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'TEMPO/create_band.html', context)

    form.save()

    user_profile = Profile.objects.get(user=request.user)
    band = get_object_or_404(Band, band_name=form.cleaned_data.get('band_name'))
    user_profile.band = band
    user_profile.save()
    return redirect(reverse('my-band'))


@login_required
@transaction.atomic
def my_band(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    band = user_profile.band
    members = Band.get_members(band)
    context = {'cur_user': request.user, 'band': band, 'members': members, 'form': AddBandUserForm()}
    return render(request, 'TEMPO/band_profile.html', context)


@login_required
@transaction.atomic
def add_event(request):
    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = EventForm()
        return render(request, 'TEMPO/add_event.html', context)

    profile = get_object_or_404(Profile, user=request.user)
    band = profile.band

    form = EventForm(request.POST, request.FILES)

    if not form.is_valid():
        context['form'] = form
        return render(request, 'TEMPO/add_event.html', context)

    event = form.save()
    band.bandevent_set.add(event)

    return redirect(reverse('live-session'))


@login_required
@transaction.atomic
def delete_event(request, id):
    event_to_delete = get_object_or_404(BandEvent, id=id)
    event_to_delete.delete()

    return HttpResponse("Successful")


# Get the user profile photo
@login_required
@transaction.atomic
def get_profile_photo(request, id):
    profile = get_object_or_404(Profile, user_id=id)
    if not profile.picture:
        raise Http404

    content_type = guess_type(profile.picture.name)
    return HttpResponse(profile.picture, content_type=content_type)


# Get the band photo
@login_required
@transaction.atomic
def get_band_photo(request, name):
    band = get_object_or_404(Band, band_name=name)
    if not band.band_photo:
        raise Http404

    content_type = guess_type(band.band_photo.name)
    return HttpResponse(band.band_photo, content_type=content_type)


# Get the event photo
@login_required
@transaction.atomic
def get_event_photo(request, id):
    event = get_object_or_404(BandEvent, id=id)
    if not event.poster_photo:
        raise Http404

    content_type = guess_type(event.poster_photo.name)
    return HttpResponse(event.poster_photo, content_type=content_type)


# Update the event status
@login_required
@transaction.atomic
def update_event(request, id):
    event = get_object_or_404(BandEvent, id=id)
    event.is_live = True
    event.save()
    return HttpResponse("")


# Start the event stream by event id
@login_required
@transaction.atomic
def start_event(request, id):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    event = get_object_or_404(BandEvent, id=id)
    event.is_live = True
    event.save()
    band = event.band
    context = {'user': user, 'profile': profile, 'event': event, 'is_starter': "T", "band": band}
    return render(request, "TEMPO/video.html", context)


# Start to watch the event by event id
@login_required
@transaction.atomic
def watch_event(request, id):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    event = get_object_or_404(BandEvent, id=id)
    band = event.band
    context = {'user': user, 'profile': profile, 'event': event, 'is_starter': "F", "band": band}
    return render(request, "TEMPO/video.html", context)


@login_required
@transaction.atomic
def get_upcoming(request, id):
    event = get_object_or_404(BandEvent, id=id)
    context = {'event': event}
    return render(request, "TEMPO/upcoming_event.html", context)


@login_required
@transaction.atomic
def end_event(request, id):
    event = get_object_or_404(BandEvent, id=id)
    event.is_live = False
    event.is_end = True
    event.save()
    return HttpResponse("")


@transaction.atomic
def forget_password(request):
    context = {}
    if request.method == 'GET':
        context['form'] = ForgetPasswordForm()
        return render(request, 'TEMPO/forget_password.html', context)

    form = ForgetPasswordForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'TEMPO/forget_password.html', context)

    form.save()

    return redirect(reverse('login'))


@login_required
@transaction.atomic
def practice_session(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    band = user_profile.band
    practice_session = PracticeSession.objects.filter(band=band)
    context = {'band': band, 'practice_session': practice_session}
    return render(request, 'TEMPO/band_practice_session.html', context)


@login_required
@transaction.atomic
def live_session(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    band = user_profile.band
    events = BandEvent.objects.filter(band=band)
    context = {'band': band, 'events': events, 'user': user_profile.user}
    return render(request, 'TEMPO/band_live_session.html', context)


@login_required
@transaction.atomic
def add_practice_session(request):
    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = PracticeSessionForm()
        return render(request, 'TEMPO/add_practice_session.html', context)

    profile = get_object_or_404(Profile, user=request.user)
    band = profile.band

    form = PracticeSessionForm(request.POST)

    if not form.is_valid():
        context['form'] = form
        return render(request, 'TEMPO/add_practice_session.html', context)

    practice_session = form.save()
    band.practicesession_set.add(practice_session)

    return redirect(reverse('practice-session'))


@login_required
@transaction.atomic
def start_practice(request, id):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    practice_session = get_object_or_404(PracticeSession, id=id)
    practice_session.is_live = True
    practice_session.starter = user.username
    practice_session.save()
    context = {'user': user, 'profile': profile, 'practice_session': practice_session, 'is_starter': 'T',
               'starter_name': user.username, 'band': profile.band}
    return render(request, "TEMPO/multi_video.html", context)


@login_required
@transaction.atomic
def join_practice(request, id):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    practice_session = get_object_or_404(PracticeSession, id=id)
    context = {'user': user, 'profile': profile, 'practice_session': practice_session, 'is_starter': 'F',
               'starter_name': practice_session.starter}
    return render(request, "TEMPO/multi_video.html", context)


@login_required
@transaction.atomic
def delete_practice(request, id):
    practice_to_delete = get_object_or_404(PracticeSession, id=id)
    practice_to_delete.delete()

    return HttpResponse("Successful")


@login_required
@transaction.atomic
def end_practice(request, id):
    practice_session = get_object_or_404(PracticeSession, id=id)
    practice_session.is_end = True
    practice_session.is_live = False
    practice_session.save()
    return HttpResponse("")


@login_required
@transaction.atomic
def add_band_user(request):
    cur_user_profile = Profile.objects.get(user=request.user)
    form = AddBandUserForm(request.POST, band=cur_user_profile.band)
    if not form.is_valid():
        return HttpResponse(form.errors['username'])

    add_user = get_object_or_404(User, username=form.cleaned_data['username'])
    user_profile = get_object_or_404(Profile, user=add_user)
    user_profile.band = cur_user_profile.band
    user_profile.save()

    return HttpResponse("Successful")


@login_required
@transaction.atomic
def delete_band_user(request, name):
    delete_user = get_object_or_404(User, username=name)
    if not delete_user == request.user:
        delete_user_profile = get_object_or_404(Profile, user=delete_user)
        delete_user_profile.band = None
        delete_user_profile.save()

    return redirect(reverse('my-band'))


@login_required
@transaction.atomic
def update_band_profile(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    band = user_profile.band
    members = Band.get_members(band)

    if request.method == 'GET':
        band_profile_form = BandProfileForm(instance=request.user.profile.band)
        context = {'cur_user': request.user, 'form': band_profile_form, 'band': band, 'members': members}
        return render(request, 'TEMPO/update_band_profile.html', context)

    band_profile_form = BandProfileForm(request.POST, request.FILES, instance=request.user.profile.band)
    if not band_profile_form.is_valid():
        context = {'cur_user': request.user, 'form': band_profile_form, 'band': band, 'members': members}
        return render(request, 'TEMPO/update_band_profile.html', context)

    band_profile_form.save()
    return redirect(reverse('my-band'))


@login_required
@transaction.atomic
def band_calendar(request):
    context = {}
    return render(request, 'TEMPO/band_calendar.html', context)


@login_required
@transaction.atomic
def band_events(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    events = BandEvent.objects.filter(band=user_profile.band)
    practice_sessions = PracticeSession.objects.filter(band=user_profile.band)
    event_list = []
    for event in events:
        title = event.name
        start = event.date_time.strftime("%Y-%m-%d")

        json_event = {'title': title, 'start': start, 'textColor': '#00CC99'}
        event_list.append(json_event)

    for event in practice_sessions:
        title = event.name
        start = event.date_time.strftime("%Y-%m-%d")

        json_event = {'title': title, 'start': start, 'textColor': '#bce8f1'}
        event_list.append(json_event)

    return HttpResponse(json.dumps(event_list), content_type="application/json")


@login_required
@transaction.atomic
def add_to_user_calendar(request):
    event = get_object_or_404(BandEvent, id=request.POST['event_id'])
    user_profile = get_object_or_404(Profile, user=request.user)

    if event in user_profile.subscribe_events.all():
        return HttpResponse("This event is already in your calendar!")

    user_profile.subscribe_events.add(event)
    user_profile.save()

    return HttpResponse("Add successfully!")


@login_required
@transaction.atomic
def user_calendar(request):
    return render(request, "TEMPO/user_calendar.html", {})


@login_required
@transaction.atomic
def user_events(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    events = user_profile.subscribe_events.all()

    event_list = []
    for event in events:
        start = event.date_time.strftime("%Y-%m-%d")

        json_event = {'id': event.id,
                      'title': event.name,
                      'start': start,
                      'date': start,
                      'location': event.location,
                      'band_name': event.band.band_name,
                      'band_description': event.band.band_description,
                      'textColor': '#00CC99'}
        event_list.append(json_event)

    return HttpResponse(json.dumps(event_list), content_type="application/json")

@login_required
@transaction.atomic
def delete_from_user_calendar(request):
    event = get_object_or_404(BandEvent, id=request.POST['event_id'])
    user_profile = get_object_or_404(Profile, user=request.user)
    user_profile.subscribe_events.remove(event)
    user_profile.save()

    return HttpResponse("")

@login_required
@transaction.atomic
def song_list(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    band_event = BandEvent.objects.filter(band=profile.band)
    return render(request, "TEMPO/band_song_lists.html", {'band_event': band_event})

@login_required
@transaction.atomic
def song(request, id):
    event = get_object_or_404(BandEvent, id=id)
    songs = event.songlist_set.all()
    form = SongForm()
    return render(request, 'TEMPO/songs.html', {'band_event': event, 'songs': songs, 'form': form})

@login_required
@transaction.atomic
def add_new_song(request, id):
    context = {}

    form = SongForm(request.POST, request.FILES)
    if not form.is_valid():
        context['form'] = form
        return HttpResponse('Fields are required!')

    song = form.save()
    event = get_object_or_404(BandEvent, id=id)
    event.songlist_set.add(song)
    return HttpResponse("Add successfully!")

@login_required
@transaction.atomic
def delete_song(request, id):
    song_deleted = get_object_or_404(SongList, id=id)
    event = song_deleted.band_event
    song_deleted.delete()

    return redirect(reverse('songs', kwargs={'id': event.id}))

# Get the event photo
@login_required
@transaction.atomic
def get_music_score(request, id):
    song = get_object_or_404(SongList, id=id)
    if not song.music_score:
        raise Http404

    content_type = guess_type(song.music_score.name)
    return HttpResponse(song.music_score, content_type=content_type)

