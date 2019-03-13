from django.contrib import admin
from .models import Song, Musician, Album, Band


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
	pass


@admin.register(Musician)
class MusicianAdmin(admin.ModelAdmin):
	pass


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
	pass


@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
	pass