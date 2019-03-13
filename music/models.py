from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from multiselectfield import MultiSelectField

from datetime import date


INSTRUMENTS = (
	('Wokal', 'Wokal'),
	('Gitara klasyczna', 'Gitara klasyczna'),
	('Gitara elektryczna', 'Gitara elektryczna'),
	('Gitara basowa', 'Gitara basowa'),
	('Perkusja', 'Perkusja'),
	('Klawisze', 'Klawisze'),
	('Pianino', 'Pianino'),
	('Skrzypce', 'Skrzypce'),
	('Flet', 'Flet'),
	('Wiolonczela', 'Wiolonczela')
)

GENRES = (
	('Blues', 'Blues'),
	('Country', 'Country'),
	('Elektroniczna', 'Elektroniczna'),
	('Folk', 'Folk'),
	('Hip hop', 'Hip hop'),
	('Jazz', 'Jazz'),
	('Klasyczna', 'Klasyczna'),
	('Latynoska', 'Latynoska'),
	('Pop', 'Pop'),
	('R & B and soul', 'R & B and soul'),
	('Rock', 'Rock')
)


class Band(models.Model):

	name = models.CharField(
		verbose_name='Nazwa zespołu',
		max_length=128
	)
	description = models.TextField(
		verbose_name='Opis',
		null=True,
		blank=True
	)
	creation_year = models.PositiveSmallIntegerField(
		verbose_name='Rok założenia',
		null=True,
		blank=True,
		validators=[MinValueValidator(1800), MaxValueValidator(date.today().year)]
	)
	genre = models.CharField(
		verbose_name='Gatunek',
		choices=GENRES,
		max_length=30
	)
	cover_image = models.ImageField(
		verbose_name='Zdjęcie zespołu',
		null=True,
		blank=True,
		upload_to='bands/%Y/%m/%d',
	)
	spotify_follow = models.CharField(
		verbose_name='Przycisk obserwowania Spotify',
		max_length=255,
		null=True,
		blank=True
	)
	spotify_play = models.CharField(
		verbose_name='Przycisk odtwarzania Spotify',
		max_length=255,
		null=True,
		blank=True
	)


class Album(models.Model):

	name = models.CharField(
		verbose_name='Nazwa albumu',
		max_length=128
	)
	cover_image = models.ImageField(
		verbose_name='Okładka',
		null=True,
		blank=True,
		upload_to='album_covers/%Y/%m/%d',
	)
	genre = models.CharField(
		verbose_name='Gatunek',
		choices=GENRES,
		max_length=30
	)
	band = models.ForeignKey(
		Band,
		verbose_name='Zespół',
		on_delete=models.CASCADE
	)
	creation_year = models.PositiveSmallIntegerField(
		verbose_name='Rok wydania',
		null=True,
		blank=True,
		validators=[MinValueValidator(1800), MaxValueValidator(date.today().year)]
	)
	spotify_play = models.CharField(
		verbose_name='Przycisk odtwarzania Spotify',
		max_length=255,
		null=True,
		blank=True
	)


class Song(models.Model):

	name = models.CharField(
		verbose_name='Tytuł piosenki',
		max_length=64
	)
	duration = models.DurationField(
		verbose_name='Długość'
	)
	album_order_no = models.PositiveSmallIntegerField(
		verbose_name='Numer'
	)
	album = models.ForeignKey(
		Album,
		verbose_name='Album',
		on_delete=models.CASCADE
	)
	lyrics = models.TextField(
		verbose_name='tekst nagrania',
		null=True,
		blank=True
	)
	spotify_play = models.CharField(
		verbose_name='Przycisk odtwarzania Spotify',
		max_length=255,
		null=True,
		blank=True
	)


class Musician(models.Model):

	name = models.CharField(
		verbose_name='Imię',
		max_length=160
	)
	date_of_birth = models.DateField(
		verbose_name='Data urodzenia',
		null=True,
		blank=True
	)
	instruments = MultiSelectField(
		verbose_name='Instrumenty',
		choices=INSTRUMENTS
	)
	band = models.ForeignKey(
		Band,
		verbose_name='Zaspół',
		on_delete=models.CASCADE
	)
