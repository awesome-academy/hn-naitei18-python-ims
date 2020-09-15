from django.test import TestCase

from myalbums.models import *

class ReviewModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name_category='dung')
        song = Song.objects.create(title="mylove",category=Category.objects.get(id=1))
        song.save()
        artist = song.artist.create(name_artist="testtag")
        artist.save()
        album = song.album.create(name_album='Dung')
        album.save()
        User.objects.create(email='dung@gmail.com',username='dung',password='1')
        Review.objects.create(content_review='Dung',song_review=Song.objects.get(id=1),user_review=User.objects.get(id=1) ,rating =3)

    def test_content_review_label(self):
        review = Review.objects.get(id=1)
        field_label = review._meta.get_field('content_review').verbose_name
        self.assertEquals(field_label,'content review')

    def test_content_review_max_length(self):
        review = Review.objects.get(id=1)
        max_length = review._meta.get_field('content_review').max_length
        self.assertEquals(max_length, 1000)

    def test_song_review_label(self):
        review = Review.objects.get(id=1)
        field_label = review._meta.get_field('song_review').verbose_name
        self.assertEquals(field_label,'song review')

    def test_user_review_label(self):
        review = Review.objects.get(id=1)
        field_label = review._meta.get_field('user_review').verbose_name
        self.assertEquals(field_label,'user review')

    def test_date_review_label(self):
        review = Review.objects.get(id=1)
        field_label = review._meta.get_field('date_review').verbose_name
        self.assertEquals(field_label,'date review')
        
    def test_rating_label(self):
        review = Review.objects.get(id=1)
        field_label = review._meta.get_field('rating').verbose_name
        self.assertEquals(field_label,'rating')


from django.test import TestCase
from myalbums.models import *

class ArtistModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Artist.objects.create(name_artist='Ly',biography='hello world')

    def test_name_artist_label(self):
        artist = Artist.objects.get(id=1)
        field_label = artist._meta.get_field('name_artist').verbose_name
        self.assertEquals(field_label,'name artist')

    def test_name_artist_max_length(self):
        artist = Artist.objects.get(id=1)
        max_length = artist._meta.get_field('name_artist').max_length
        self.assertEquals(max_length, 50)

    def test_birthday_label(self):
        artist = Artist.objects.get(id=1)
        field_label = artist._meta.get_field('birthday').verbose_name
        self.assertEquals(field_label,'birthday')

    def test_biography_label(self):
        artist = Artist.objects.get(id=1)
        field_label = artist._meta.get_field('biography').verbose_name
        self.assertEquals(field_label,'biography')

    def test_biography_max_length(self):
        artist = Artist.objects.get(id=1)
        max_length = artist._meta.get_field('biography').max_length
        self.assertEquals(max_length, 400)

    def test_get_absolute_url(self):
        artist = Artist.objects.get(id=1)
        self.assertEquals(artist.get_absolute_url(), '/artist/1')