from django.contrib import admin
import numpy as np

# Register your models here.
from .models import Song, Artist, Category, Album, Review, User


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'hot')
    # fields = ['title']


# class SongInline(admin.TabularInline):
#     model = Song


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['name_category']
#     inlines = [SongInline]


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    fields = ['name_album']
#     inlines = [SongInline]


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    #     list_display = ('name_artist', 'birthday')
    fields = ['name_artist']

# @admin.register(Favourite)
# @admin.register(Follower)
# @admin.register(Comment)
# @admin.register(Lyric)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('song_review', 'user_review',
                    'content_review', 'date_review', 'rating')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password')
