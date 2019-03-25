from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse

from users.forms import CommentForm
from users.views import prev_page
from .forms import SearchForm, CreateBandForm, CreateAlbumForm, CreateSongForm, CreateMusicianForm
from .models import Band, Album, Musician, Song, GENRES, INSTRUMENTS
from .my_context_processor import genres
from users.models import Comment

import random
from datetime import timedelta

from faker import Faker
from tqdm import trange


class SearchView(View):

	def get(self, request):
		search_choices = request.session.get('search_choices')
		form = SearchForm(initial=(search_choices))
		return render(request, 'search.html', {'form': form})

	def post(self, request):
		form = SearchForm(request.POST)
		if form.is_valid():
			bands = Band.objects.all()
			albums = Album.objects.all()
			songs = Song.objects.all()
			# if clicked on genre button filter results
			for genre in genres(None)['genres']:
				if request.POST.get(genre):
					bands = bands.filter(genre=genre)
					albums = albums.filter(genre=genre)
					songs = songs.filter(album__genre=genre)
			# storing form data
			name = '' if request.POST.get('all') else form.cleaned_data['search_field']
			checked_bands = form.cleaned_data['search_bands']
			checked_albums = form.cleaned_data['search_albums']
			checked_songs = form.cleaned_data['search_songs']
			# defining type of results, mixing it in python's list
			# saves choices to session
			results = []
			search_choices = {}
			if checked_bands:
				results = list(bands.filter(name__icontains=name))
				search_choices['search_bands'] = True
			else:
				search_choices['search_bands'] = False

			if checked_albums:
				results += list(albums.filter(name__icontains=name))
				search_choices['search_albums'] = True
			else:
				search_choices['search_albums'] = False

			if checked_songs:
				results += list(songs.filter(name__icontains=name))
				search_choices['search_songs'] = True
			else:
				search_choices['search_songs'] = False

			request.session['search_choices'] = search_choices
			# new form because it stays for new searching
			new_form = SearchForm(initial=(search_choices))
			# ordering results by name
			results = sorted(results, key=lambda x: x.name)

			ctx = {
				'results': results,
				'form': new_form,
			}
			return render(request, 'search_results.html', ctx)


class BandView(View):

	def get(self, request, band_id):
		band = Band.objects.get(id=band_id)
		musicians = Musician.objects.filter(band=band)
		albums = Album.objects.filter(band=band)
		comments = Comment.objects.filter(band=band)
		form = CommentForm(initial={
			'band': band,
			'author': request.user
		})

		ctx = {
			'band': band,
			'musicians': musicians,
			'albums': albums,
			'comments': comments,
			'form': form
		}
		return render(request, 'band.html', ctx)


class CreateBandView(UserPassesTestMixin, View):

	def test_func(self):
		return self.request.user.is_staff or self.request.user.is_superuser

	def get(self, request):
		form = CreateBandForm()
		ctx = {
			'form': form,
			'title': 'Dodawanie nowego zespołu',
		}
		return render(request, 'creation_form.html', ctx)

	def post(self, request):
		form = CreateBandForm(request.POST, request.FILES)
		if form.is_valid():
			article = form.save()
			return redirect('article', article_id=article.id)


class ModifyBandView(UserPassesTestMixin, View):

	def test_func(self):
		return self.request.user.is_staff or self.request.user.is_superuser

	def get(self, request, band_id):
		band = Band.objects.get(id=band_id)
		form = CreateBandForm(initial=model_to_dict(band))
		ctx = {
			'form': form,
			'title': 'Edycja zespołu'
		}
		return render(request, 'creation_form.html', ctx)

	def post(self, request, band_id):
		band = Band.objects.get(id=band_id)
		form = CreateBandForm(request.POST, request.FILES, instance=band)
		if form.is_valid():
			form.save()
			return redirect('band', band_id=band.id)


class DeleteBandView(UserPassesTestMixin, View):

	def test_func(self):
		return self.request.user.is_staff or self.request.user.is_superuser

	def get(self, request, band_id):
		band = Band.objects.get(id=band_id)
		band.delete()
		return redirect(prev_page(request))


class CreateMusicianView(UserPassesTestMixin, View):

	def test_func(self):
		return self.request.user.is_staff or self.request.user.is_superuser

	def get(self, request, band_id):
		band = Band.objects.get(id=band_id)
		form = CreateMusicianForm(initial={'band': band})
		ctx = {
			'form': form,
			'title': 'Dodawanie nowego muzyka',
		}
		return render(request, 'creation_form.html', ctx)

	def post(self, request, band_id):
		form = CreateMusicianForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('band', band_id=band_id)


class DeleteMusicianView(UserPassesTestMixin, View):

	def test_func(self):
		return self.request.user.is_staff or self.request.user.is_superuser

	def get(self, request, musician_id):
		musician = Musician.objects.get(id=musician_id)
		musician.delete()
		return redirect(prev_page(request))


class AlbumView(View):

	def get(self, request, album_id):
		album = Album.objects.get(id=album_id)
		songs = Song.objects.filter(album=album).order_by('album_order_no')
		comments = Comment.objects.filter(album=album)
		form = CommentForm(initial={
			'album': album,
			'author': request.user
		})

		ctx = {
			'album': album,
			'songs': songs,
			'comments': comments,
			'form': form
		}
		return render(request, 'album.html', ctx)


class CreateAlbumView(UserPassesTestMixin, View):

	def test_func(self):
		return self.request.user.is_staff or self.request.user.is_superuser

	def get(self, request, band_id):
		form = CreateAlbumForm(initial={'band': Band.objects.get(id=band_id)})
		ctx = {
			'form': form,
			'title': 'Dodawanie nowego albumu',
		}
		return render(request, 'creation_form.html', ctx)

	def post(self, request, band_id):
		form = CreateAlbumForm(request.POST, request.FILES)
		if form.is_valid():
			album = form.save()
			return redirect('album', album_id=album.id)


class ModifyAlbumView(UserPassesTestMixin, View):

	def test_func(self):
		return self.request.user.is_staff or self.request.user.is_superuser

	def get(self, request, album_id):
		album = Album.objects.get(id=album_id)
		form = CreateAlbumForm(initial=model_to_dict(album))
		ctx = {
			'form': form,
			'title': 'Edycja albumu'
		}
		return render(request, 'creation_form.html', ctx)

	def post(self, request, album_id):
		album = Album.objects.get(id=album_id)
		form = CreateAlbumForm(request.POST, request.FILES, instance=album)
		if form.is_valid():
			form.save()
			return redirect('album', album_id=album.id)


class DeleteAlbumView(UserPassesTestMixin, View):

	def test_func(self):
		return self.request.user.is_staff or self.request.user.is_superuser

	def get(self, request, album_id):
		album = Album.objects.get(id=album_id)
		album.delete()
		return redirect(prev_page(request))


class SongView(View):

	def get(self, request, song_id):
		song = Song.objects.get(id=song_id)
		comments = Comment.objects.filter(song=song)
		form = CommentForm(initial={
			'song': song,
			'author': request.user
		})

		ctx = {
			'song': song,
			'comments': comments,
			'form': form
		}
		return render(request, 'song.html', ctx)


class CreateSongView(UserPassesTestMixin, View):

	def test_func(self):
		return self.request.user.is_staff or self.request.user.is_superuser

	def get(self, request, album_id):
		album = Album.objects.get(id=album_id)
		form = CreateSongForm(initial={'album': album})
		ctx = {
			'form': form,
			'title': 'Dodawanie nowego utworu',
		}
		return render(request, 'creation_form.html', ctx)

	def post(self, request, album_id):
		form = CreateSongForm(request.POST)
		if form.is_valid():
			song = form.save()
			return redirect('song', song_id=song.id)


class ModifySongView(UserPassesTestMixin, View):

	def test_func(self):
		return self.request.user.is_staff or self.request.user.is_superuser

	def get(self, request, song_id):
		song = Song.objects.get(id=song_id)
		form = CreateSongForm(initial=model_to_dict(song))
		ctx = {
			'form': form,
			'title': 'Edycja utworu'
		}
		return render(request, 'creation_form.html', ctx)

	def post(self, request, song_id):
		song = Song.objects.get(id=song_id)
		form = CreateSongForm(request.POST, request.FILES, instance=song)
		if form.is_valid():
			form.save()
			return redirect('song', song_id=song.id)


class DeleteSongView(UserPassesTestMixin, View):

	def test_func(self):
		return self.request.user.is_staff or self.request.user.is_superuser

	def get(self, request, song_id):
		song = Song.objects.get(id=song_id)
		song.delete()
		return redirect(prev_page(request))


class AddFakeMusicView(UserPassesTestMixin, View):

	def test_func(self):
		return self.request.user.is_superuser

	def get(self, request):
		# creates fake music data
		fake = Faker('pl_PL')
		users = User.objects.all()
		# create band
		for band_create in trange(1, 51):
			band = Band.objects.create(
				name=random.choice((fake.word(), fake.word(), fake.sentence())),
				description=fake.text(),
				genre=random.choice(GENRES)[0],
				creation_year=random.randint(1900, 2019)
			)
			# create comments for band
			for _ in range(1, random.randint(1, 10)):
				Comment.objects.create(
					author=random.choice(users),
					comment=fake.sentence(),
					band=band)
			# create musicians for band
			for _ in range(1, random.randint(1, 7)):
				Musician.objects.create(
					name=fake.name(),
					instruments=[random.choice(INSTRUMENTS)[0] for _ in range(1, random.randint(1, 4))],
					band=band
				)
			# create albums for band
			for _ in range(1, random.randint(2, 7)):
				album = Album.objects.create(
					name=random.choice((fake.word(), fake.word() + fake.word(), fake.word() + fake.word() + fake.word())),
					genre=band.genre,
					band=band,
					creation_year=random.randint(band.creation_year, 2019)
				)
				# create comments for album
				for _ in range(1, random.randint(1, 10)):
					Comment.objects.create(
						author=random.choice(users),
						comment=fake.sentence(),
						album=album)
				# create songs for album
				for no in range(6, random.randint(6, 14)):
					lyrics = ''
					for row in range(16):
						lyrics += f'<p>{fake.sentence()}</p>'
					song = Song.objects.create(
						name=random.choice((fake.word(), fake.sentence())),
						album_order_no=no,
						album=album,
						lyrics=lyrics,
						duration=timedelta(
							minutes=random.randint(2, 6),
							seconds=random.randint(0, 59)
						)
					)
					# create comments for song
					for _ in range(1, random.randint(1, 10)):
						Comment.objects.create(
							author=random.choice(users),
							comment=fake.sentence(),
							song=song)

		return HttpResponse('Zrobione')

