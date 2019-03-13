from django.db import models
from django.contrib.auth import get_user_model
from music.models import Band, Album


class Article(models.Model):

	author = models.ForeignKey(
		get_user_model(),
		verbose_name='Autor artykułu',
		on_delete=models.SET_NULL,
		null=True
	)
	title = models.CharField(
		verbose_name='Tytuł artykułu',
		max_length=255
	)
	content = models.TextField(
		verbose_name='Treść artykułu'
	)
	creation_date = models.DateTimeField(
		auto_now_add=True,
		blank=True
	)
	modification_date = models.DateTimeField(
		null=True,
		blank=True
	)
	cover_image = models.ImageField(
		verbose_name='Zdjęcie',
		null=True,
		blank=True,
		upload_to='article_covers/%Y/%m/%d'
	)
