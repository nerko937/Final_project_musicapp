from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError
from articles.models import Article
from music.models import Band, Album, Song


class Comment(models.Model):

	author = models.ForeignKey(
		get_user_model(),
		verbose_name='Autor komentarza',
		on_delete=models.CASCADE
	)
	comment = models.TextField(
		verbose_name='Komentarz'
	)
	creation_date = models.DateTimeField(
		auto_now_add=True,
		blank=True
	)
	modification_date = models.DateTimeField(
		null=True,
		blank=True
	)
	article = models.ForeignKey(
		Article,
		verbose_name='Artykuł',
		on_delete=models.CASCADE,
		null=True,
		blank=True
	)
	band = models.ForeignKey(
		Band,
		verbose_name='Zespół',
		on_delete=models.CASCADE,
		null=True,
		blank=True
	)
	album = models.ForeignKey(
		Album,
		verbose_name='Płyta',
		on_delete=models.CASCADE,
		null=True,
		blank=True
	)
	song = models.ForeignKey(
		Song,
		verbose_name='Nagranie',
		on_delete=models.CASCADE,
		null=True,
		blank=True
	)

	def clean(self):
		# checks if comment is assigned to only one parent model
		validation_list = []

		if self.article:
			validation_list.append(0)
		if self.band:
			validation_list.append(0)
		if self.album:
			validation_list.append(0)
		if self.song:
			validation_list.append(0)

		if len(validation_list) != 1:
			raise ValidationError(
				'Komentarz może być przypisany tylko do jednego - artykułu, zespołu lub płyty'
			)
