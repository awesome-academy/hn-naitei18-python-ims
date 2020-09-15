from django.test import TestCase
from django.urls import reverse

from myalbums.models import *

class ReviewAddTest(TestCase):
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

    def test_view_url_exists_at_desired_location(self):
        review = Review.objects.get(id=1)
        song = Song.objects.get(id=1)
        url = '/review/1/create'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
           
    def test_view_url_accessible_by_name(self):
        song = Song.objects.get(id=1)
        url = reverse('review_create',  args=[str(song.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

from django.test import TestCase
from django.urls import reverse
from myalbums.models import *

class ArtistListViewTest(TestCase):
    @classmethod

    def setUpTestData(cls):
        Artist.objects.create(name_artist='Ly',biography='hello world')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/artist/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('artist'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('artist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myalbums/artist_list.html')
