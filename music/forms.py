from django import forms

from music.models import Band, Album, Song, Musician


class SearchForm(forms.Form):

	search_field = forms.CharField(
		required=False,
		label='',
		max_length=64,
		widget=forms.TextInput(attrs={'class': 'form-control'})
	)
	search_bands = forms.BooleanField(
		required=False,
		initial=True,
		label='',
		widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
	)
	search_albums = forms.BooleanField(
		required=False,
		initial=True,
		label='',
		widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
	)
	search_songs = forms.BooleanField(
		required=False,
		label='',
		widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
	)


class CreateBandForm(forms.ModelForm):

	class Meta:
		model = Band
		fields = '__all__'


class CreateMusicianForm(forms.ModelForm):

	class Meta:
		model = Musician
		fields = '__all__'
		widgets = {'band': forms.HiddenInput()}


class CreateAlbumForm(forms.ModelForm):

	class Meta:
		model = Album
		fields = '__all__'
		widgets = {'band': forms.HiddenInput()}


class CreateSongForm(forms.ModelForm):

	class Meta:
		model = Song
		fields = '__all__'
		widgets = {
			'album': forms.HiddenInput(),
			'lyrics': forms.HiddenInput(),
			'duration': forms.TextInput(attrs={'placeholder': 'godziny:minuty:sekundy'})
		}