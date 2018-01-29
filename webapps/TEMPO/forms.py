from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.contrib.auth.models import User

# Define the login form
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='username',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        required=True)
    password = forms.CharField(
        label='password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        required=True)

# Define the registration form
class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'placeholder': 'English letters and numbers'}))
    first_name = forms.CharField(max_length=200,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=200,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    password1 = forms.CharField(max_length=200,
                                label='Password',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=200,
                                label='Confirm Password',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    email_address = forms.CharField(max_length=200,
                                    label='email',
                                    widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))

    # Override the forms.form .clean function
    def clean(self):
        # Call parent (forms.Form).clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirm the two password field match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent
        return cleaned_data

    # Customized the validation for username field
    def clean_username(self):
        # Confirm the username is not already present in
        # the User model form
        username = self.cleaned_data.get('username')
        if not username.isalnum():
            raise forms.ValidationError("Username must only contain English alphabet and number")
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # return the username
        return username


class BandForm(forms.ModelForm):
    class Meta:
        model = Band
        fields = ('band_name', 'band_description', 'band_photo')
        widgets = {'band_name': forms.TextInput(attrs={'placeholder': 'English letters and numbers'}),
                   'band_description': forms.Textarea(attrs={'placeholder': 'Describe your band...',
                                                             'rows': 8,
                                                             'cols': 40, }),
                   'band_photo': forms.FileInput()}

    def clean_band_name(self):
        cleaned_data = super(BandForm, self).clean()
        band_name = cleaned_data.get('band_name')

        if not band_name.isalnum():
            raise forms.ValidationError("Band name must only contain English alphabet and number")

        return band_name


class EventForm(forms.ModelForm):
    class Meta:
        model = BandEvent
        fields = ('name', 'date_time', 'location', 'poster_photo')
        widgets = {'name': forms.TextInput(attrs={'placeholder': 'Event Name'}),
                   'date_time': forms.DateInput(attrs={'placeholder': 'Valid Format:YYYY-MM-DD'}),
                   'location': forms.TextInput(attrs={'placeholder': 'location'}),
                   'poster_photo': forms.FileInput()}


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birthday', 'age', 'location', 'bio', 'picture')
        widgets = {'birthday': forms.DateInput(attrs={'placeholder': 'Valid Format:YYYY-MM-DD'}), 'picture': forms.FileInput()}

class SongForm(forms.ModelForm):
    class Meta:
        model = SongList
        fields = ('song_name', 'music_score')
        widgets = {'song_name': forms.TextInput(attrs={'placeholder': 'Song Name'}),
                   'music_score': forms.FileInput()}


class BandProfileForm(forms.ModelForm):
    class Meta:
        model = Band
        fields = ('band_description', 'band_photo')
        widgets = {'band_description': forms.Textarea(attrs={'placeholder': 'Describe your band...',
                                                             'rows': 8,
                                                             'cols': 40, }),
                   'band_photo': forms.FileInput()}


class ForgetPasswordForm(forms.Form):
    username = forms.CharField(max_length=200,
                               widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(max_length=200,
                                widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))
    password2 = forms.CharField(max_length=200,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    def clean(self):
        cleaned_data = super(ForgetPasswordForm, self).clean()

        username = cleaned_data.get('username')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if not User.objects.filter(username__exact=username):
            raise forms.ValidationError("The username does not exist")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        return cleaned_data

    def save(self):
        user = User.objects.get(username=self.cleaned_data['username'])
        user.set_password(self.cleaned_data['password1'])
        user.save()

class PracticeSessionForm(forms.ModelForm):
    class Meta:
        model = PracticeSession
        fields = ('name', 'date_time')
        widgets = {'name': forms.TextInput(attrs={'placeholder': 'Event Name'})}

class AddBandUserForm(forms.Form):
    username = forms.CharField(max_length=200,
                               label="Username",
                               widget=forms.TextInput(attrs={'placeholder': 'Username'}))

    def __init__(self, *args, **kwargs):
        self.band = kwargs.pop('band', None)
        super(AddBandUserForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not username.isalnum():
            raise forms.ValidationError("Username must only contain English alphabet and number.")

        user = User.objects.filter(username__exact=username)
        if not user:
            raise forms.ValidationError("Username doesn't exist.")

        user = User.objects.get(username=username)
        members = Profile.objects.filter(band=self.band)
        user_profile = Profile.objects.get(user=user)
        if user_profile in members:
            raise forms.ValidationError("User is already a member of your band.")

        # return the username
        return username
