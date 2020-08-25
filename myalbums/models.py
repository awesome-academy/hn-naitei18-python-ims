from django.db import models
from django.urls import reverse
from datetime import date
from django.utils import timezone
from django.contrib.auth import get_user_model
import numpy as np
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from time import strftime, gmtime


class MyModelName(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    my_field_name = models.CharField(
        max_length=20, help_text='Enter field documentation')
    

    # Metadata
    class Meta:
        ordering = ['-my_field_name']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.my_field_name


class Category(models.Model):
    name_category = models.CharField(max_length=20, null=True, help_text=(
        'Enter a song category (e.g. Sad love)'))

    def get_absolute_url(self):
        return reverse('category-detail', args=[str(self.id)])

    def __str__(self):
        return self.name_category
    thumbnail = models.ImageField(upload_to="genres", default="default.jpeg")


class Album(models.Model):
    name_album = models.CharField(max_length=50)

    def get_absolute_url(self):
        return reverse('album-detail', args=[str(self.id)])

    def __str__(self):
        return self.name_album


class Lyric(models.Model):
    content = models.CharField(max_length=1000, null=True)
    song = models.ForeignKey('Song', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    lyric_status = models.BooleanField(default=False)

    def __str__(self):
        return self.content


class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ManyToManyField(
        'Artist', help_text='Select song for this artist')
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True)
    album = models.ManyToManyField(
        'Album', help_text='Select album for this song')
    hot = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to="thumbnails", blank=False,default="default.jpeg")
    playtime = models.CharField(max_length=10, default="0.00")

    @property
    def duration(self):
        return str(strftime('%H:%M:%S', gmtime(float(self.playtime))))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('song-detail', args=[str(self.id)])

    def display_category(self):
        return ', '.join(category.name for category in self.category.all()[:5])

    def average_rating(self):
        all_ratings = map(lambda x: x.rating, self.review_set.all())
        return np.mean(all_ratings)


class Artist(models.Model):
    name_artist = models.CharField(max_length=50)
    birthday = models.DateField(null=True, blank=True)
    biography = models.CharField(max_length=400, null=True, help_text=(
        'Enter your biography '))
    def get_absolute_url(self):
        return reverse('artist-detail', args=[str(self.id)])

    def __str__(self):
        return self.name_artist


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=20)
    password = models.CharField(None, max_length=128)

    email = models.EmailField(
        verbose_name='email address', max_length=255, unique=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    # notice the absence of a "Password field", that is built in.
    object = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    def __str__(self):
        return self.user_name

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active


class Comment(models.Model):
    review = models.ForeignKey(
        'Review', on_delete=models.CASCADE, related_name='comments')
    # comment = models.ForeignKey('Comment', max_length=200, on_delete=models.SET_NULL)
    text = models.TextField()
    date_comment = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment


class Review(models.Model):
    content_review = models.CharField(max_length=1000)
    song_review = models.ForeignKey('Song', on_delete=models.CASCADE)
    user_review = models.ForeignKey('User', on_delete=models.CASCADE)
    date_review = models.DateTimeField(default=timezone.now)
    RATING_CHOICES = (
        (1, 'so bad'),
        (2, 'bad'),
        (3, 'normal'),
        (4, 'good'),
        (5, 'so good'),
    )
    rating = models.IntegerField(choices=RATING_CHOICES)

    def __str__(self):
        return self.content_review


class Follower(models.Model):
    follower = models.ForeignKey(
        'User', related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(
        'User', related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return '%s follows %s'%(self.follower, self.following)


class Favourite(models.Model):
    favourite_name = models.CharField(max_length=50)
    user_favourite = models.ForeignKey('User', on_delete=models.CASCADE)
    song_favourite = models.ManyToManyField(
        'Song', help_text='Select song for this favourite')

    def __str__(self):
        return self.favourite_name
