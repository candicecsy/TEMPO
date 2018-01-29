from django.conf.urls import url
import django.contrib.auth.views
from TEMPO.forms import LoginForm
import TEMPO.views

urlpatterns = [
    # Route to user home page
    url(r'^$', TEMPO.views.home, name='home'),
    # Route to log in page
    url(r'^login/$', django.contrib.auth.views.login,
        {'template_name': 'TEMPO/login.html', 'authentication_form': LoginForm, 'redirect_authenticated_user': True}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout', django.contrib.auth.views.logout_then_login, name='logout'),
    # Route to register page
    url(r'^register/$', TEMPO.views.register, name='register'),
    # Route to add event page
    url(r'^add_event/$', TEMPO.views.add_event, name='add-event'),
    # Route to delete event page
    url(r'^delete_event/(?P<id>\d+)$', TEMPO.views.delete_event, name='delete-event'),
    # Route to start event page
    url(r'^video/(?P<id>\d+)$', TEMPO.views.start_event, name='start-event'),
    # Route to user profile page
    url(r'^profile/$', TEMPO.views.profile, name='profile'),
    # Route to create band page
    url(r'^create_band/$', TEMPO.views.create_band, name='create-band'),
    # Route to my band page
    url(r'^my_band/$', TEMPO.views.my_band, name='my-band'),
    # Get the user profile photo
    url(r'^user_photo/(?P<id>\d+)$', TEMPO.views.get_profile_photo, name='user-photo'),
    # Get the band photo
    url(r'^band_photo/(?P<name>[0-9a-zA-Z]+)$', TEMPO.views.get_band_photo, name='band-photo'),
    # Get the event photo
    url(r'^event_photo/(?P<id>\d+)$', TEMPO.views.get_event_photo, name='event-photo'),
    # Update the event status
    url(r'^update_event/(?P<id>\d+)$', TEMPO.views.update_event, name='update-event'),
    # Get the upcoming event introduction
    url(r'^get_upcoming/(?P<id>\d+)$', TEMPO.views.get_upcoming, name='get-upcoming'),
    # join the watching room
    url(r'^watch_event/(?P<id>\d+)$', TEMPO.views.watch_event, name='watch-event'),
    # Update the event status
    url(r'^end_event/(?P<id>\d+)$', TEMPO.views.end_event, name='end-event'),
    # Update the profile
    url(r'^update-profile', TEMPO.views.update_profile, name='update-profile'),
    # forget the password
    url(r'^forget_password', TEMPO.views.forget_password, name='forget-password'),
    # Route to the practise session
    url(r'^practice_session', TEMPO.views.practice_session, name='practice-session'),
    # Route to the live session
    url(r'^live_session', TEMPO.views.live_session, name='live-session'),
    # add the practice session
    url(r'^add_practice_session', TEMPO.views.add_practice_session, name='add-practice-session'),
    # start the practice session
    url(r'^practice/(?P<id>\d+)$', TEMPO.views.start_practice, name='start-practice'),
    # start the practice session
    url(r'^join_practice/(?P<id>\d+)$', TEMPO.views.join_practice, name='join-practice'),
    # delete the practice session
    url(r'^delete_practice/(?P<id>\d+)$', TEMPO.views.delete_practice, name='delete-practice'),
    # update the practice session status
    url(r'^end_practice/(?P<id>\d+)$', TEMPO.views.end_practice, name='end-practice'),
    # Add a new band user
    url(r'^add_band_user/$', TEMPO.views.add_band_user, name='add-band-user'),
    # Delete a band user
    url(r'^delete_band_user/(?P<name>[0-9a-zA-Z]+)$', TEMPO.views.delete_band_user, name='delete-band-user'),
    # Route to update band profile
    url(r'^update_band_profile/$', TEMPO.views.update_band_profile, name='update-band-profile'),
    # Route to band calendar
    url(r'^band_calendar/$', TEMPO.views.band_calendar, name='band-calendar'),
    # Route to band events feed to band calendar
    url(r'^band_events/$', TEMPO.views.band_events, name='band-events'),
    # Route to subscribe and add an event to user's calendar
    url(r'^add-to-user-calendar/$', TEMPO.views.add_to_user_calendar, name='add-to-user-calendar'),
    # Route to user calendar
    url(r'^user_calendar/$', TEMPO.views.user_calendar, name='user-calendar'),
    # Route to users' subscribed events feed to user calendar
    url(r'^user_events/$', TEMPO.views.user_events, name='user-events'),
    # Route to un-subscribe and delete an event from user's calendar
    url(r'^delete-from-user-calendar/$', TEMPO.views.delete_from_user_calendar, name='delete-from-user-calendar'),
    # Route to song list
    url(r'^song-list/$', TEMPO.views.song_list, name='song-list'),
    # Route to song page
    url(r'^songs/(?P<id>\d+)$', TEMPO.views.song, name='songs'),
    # Route to add a new song
    url(r'add-new-song/(?P<id>\d+)$', TEMPO.views.add_new_song, name='add-new-song'),
    # Route to delete a song
    url(r'delete-song/(?P<id>\d+)$', TEMPO.views.delete_song, name='delete-song'),
    # Route to get music score
    url(r'get-music-score/(?P<id>\d+)$', TEMPO.views.get_music_score, name='get-music-score'),
]
