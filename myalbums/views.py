from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, DeleteView, ListView
from .models import Song, Artist, Category, Album, Review, User, Profile
# from utils.song_utils import generate_key

from .forms import UserUpdateForm, ProfileUpdateForm, LyricAddForm, ReviewForm, SongUploadForm
from .forms import RegisterForm, CommentForm
from tinytag import TinyTag
from django.http import  HttpResponseRedirect
from tinytag import TinyTag
from django.views.generic.list import BaseListView
from .models import *
# from utils.song_utils import generate_key
from .forms import UserUpdateForm, ProfileUpdateForm


from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
# from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import  get_object_or_404
import ssl,smtplib
import environ
import os
# from django.utils.translation import ugettext_lazy as _

env = environ.Env()
# reading .env file
environ.Env.read_env()


def index(request):
    context = {
        'artists' : Artist.objects.all()[:6],
        'genres': Category.objects.all()[:6],
        'latest_songs': Song.objects.all(),
    }
    return render(request, "index.html", context)


class CategoryListView(ListView):
    model = Category


class CategoryDetailView(DetailView):
    model = Category

class SongListView(ListView):
    model = Song


class ArtistListView(ListView):
    model = Artist


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Successful!!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user': request.user,
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'registration/profile.html', context)


class ArtistDetailView(DetailView):
    model = Artist


class HotSongListView(ListView):
    model = Song
    template_name = 'myalbums/hot_music.html'
    context_object_name = 'songs'

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')
        data = {'username':username,'email': email, 'password1': password1, 'password1': password2}
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(password1)
            user.active = False
            user.save()
            form.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            # subject = 'Activate your blog account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # 'token':account_activation_token.make_token(user),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email], from_email=settings.EMAIL_HOST_USER
            )
            email.content_subtype = "html" 
            email.send()
            # send_mail('check', 'hello','nguyen.thi.dungb@sun-asterisk.com',['tran.van.thongb@sun-asterisk.com'],fail_silently=False,)
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

# user = get_object_or_404(User, pk=uid)
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')

    else:
        return HttpResponse('Activation link is invalid!')


class SearchSongListView(ListView):
    # template_name = 'myalbums/song_detail.html'
    model = Song
    def get_queryset(self):
        query = self.request.GET.get('search')
        if query :
            return  Song.objects.filter(title__icontains=query)
        else :
            return  Song.objects.all()

class StationListView(ListView):
    model = User
    template_name = 'myalbums/user_list.html'

@login_required()
def follow(request, pk):
    if request.method == 'GET':
        user = request.user
        to_user = get_object_or_404(User, pk=pk)
        is_followed = 0

        try:
            followed = Follow.objects.get(follower=user, following=to_user)
            if followed:
                is_followed = 1
        except:
            pass

        context = {
            'user': user,
            'to_user': to_user,
            'is_followed': is_followed,
        }
        return render(request, 'myalbums/user_detail.html', context=context)
    elif request.method == 'POST':
        user = request.user
        to_user = get_object_or_404(User, pk=pk)

        try:
            followed = Follow.objects.get(follower=user, following=to_user)
            if followed:
                followed.delete()
                content = ' Unfollowed  : ' + to_user.username
                activity = Activity(user=user, activity_type='unfollow', activity=content)
                activity.save()
        except:
            follow = Follow(follower=user, following=to_user)
            follow.save()
            content = ' Now following  : ' + to_user.username
            activity = Activity(user=user, activity_type='follow', activity=content)
            activity.save()

        url = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(url)


@login_required()
def favorite(request, pk):
    if request.method == 'GET':
        user = request.user
        favorite = get_object_or_404(Song, pk=pk)
        # review = Review.objects.get(user_review = user , song_review = favorite)
        is_favorite = 0

        try:
            favorited = Favorite.objects.get(user_favorite = user, song_favorite = favorite)
            if favorited:
                is_favorite= 1
        except:
            pass

        context = {
            'user': user,
            'favorite': favorite,
            'is_favorite': is_favorite,
            # 'review' : review,
        }
        return render(request, 'myalbums/song_detail.html', context=context)
    elif request.method == 'POST':
        user = request.user
        favorite = get_object_or_404(Song, pk=pk)

        try:
            favorited = Favorite.objects.get(user_favorite = user, song_favorite = favorite)
            if favorited:
                favorited.delete()
                content = ' Disliked : ' + favorite.title
                activity = Activity(user=user, activity_type='unfavorite', activity=content)
                activity.save()
        except:
            favorited = Favorite(user_favorite = user, song_favorite = favorite)
            favorited.save()
            content = ' Liked : ' + favorite.title
            activity = Activity(user = user, activity_type='favorite', activity= content)
            activity.save()
        url = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(url)

class FavoriteListView(ListView):
    model = Song
    template_name = 'myalbums/favorite.html'

def addlyric(request, pk):
    user = request.user
    song = get_object_or_404(Song, pk=pk)
    # content = Lyric.content
    form = LyricAddForm()
    context = {
        'user': user,
        'song': song,
        # 'content': content,
        'form': form,
    }
    if request.method == 'POST':
            form = LyricAddForm(request.POST, initial={'user': user, 'song': song})
            if form.is_valid():
                form.save()
                return redirect('song-detail', pk)

    return render(request, 'myalbums/lyric_add.html', context)

@login_required
def ReviewAdd(request, pk):
    user = request.user
    song = get_object_or_404(Song, pk=pk)
    form = ReviewForm()
    context = {
        'user': user,
        'song': song,
        'form': form,
    }
    if request.method == 'POST':
        form = ReviewForm(request.POST, initial={'user': user, 'song': song})
        if form.is_valid():
            form.save()
            content = ' had reviewed : ' + song.title
            activity = Activity(user=user, activity_type='review', activity = content)
            activity.save()
            return redirect('song-detail',pk)
    return render(request, 'myalbums/review_form.html', context)


# @login_required
# def CommentAdd(request, pk):
#     user = request.user
#     # user = form.save(commit=False)
#     review = get_object_or_404(Review, pk=pk)
#     form = CommentForm()
#     context = {
#         'user': user,
#         'review': review,
#         'form': form,
#     }
#     if request.method == 'POST':
#         form = CommentForm(request.POST, initial={'review': review})
#         if form.is_valid():
#             form.save()
#             return redirect('song-detail',pk)
#     return render(request, 'myalbums/song_detail.html', { 'form': form })



@login_required
def CommentAdd(request, pk):
    url = request.META.get('HTTP_REFERER')  # get last url
    review = get_object_or_404(Review, pk=pk)
    # comments = review.content.get(review=review)
    if request.method == 'POST':  # check post
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment()
            comment.review = review
            comment.text = form.cleaned_data['text']
            # return HttpResponse(comment.text)
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(url)
    template = 'myalbums/song_detail.html'
    context = {'form': form}
    return render(request, template, context)


class SongUploadView(CreateView):
    form_class = SongUploadForm
    template_name = "myalbums/create.html"

    @method_decorator(login_required(login_url=reverse_lazy('index')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SongUploadView, self).get_context_data(**kwargs)
        context['artists'] = Artist.objects.all()
        context['category'] = Category.objects.all()
        return context


    def post(self, request, *args, **kwargs):

        form = self.get_form()
        print(form)
        if form.is_valid():

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=200)

    def form_valid(self, form):
        song = TinyTag.get(self.request.FILES['song'].file.name)
        form.instance.playtime = song.duration
        form.instance.size = song.filesize
        artists = []
        for a in self.request.POST.getlist('artists[]'):
            try:
                artists.append(int(a))
            except:
                artist = Artist.objects.create(name=a)
                artists.append(artist)
        form.save()
        form.instance.artist.set(artists)
        form.save()
        data = {
            'status': True,
            'message': "Successfully submitted form data.",
            'redirect': reverse_lazy('song-detail', kwargs={'pk': form.instance.id})
        }
        return JsonResponse(data)

class ActivityListView(ListView):
    template_name = 'myalbums/activity_list.html'
    model = Activity
    # paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ActivityListView, self).get_context_data(**kwargs)
        followings = Follow.objects.filter(follower=self.request.user)
        user_list = [self.request.user]
        for following in followings:
            user_list.append(following.following)
        activity_list = Activity.objects.filter(user__in=user_list).order_by('-id')
        context.update({
            'history': activity_list
        })
        return context

@login_required
def CommentAdd(request, pk):
    url = request.META.get('HTTP_REFERER')  # get last url
    review = get_object_or_404(Review, pk=pk)
    # comments = review.content.get(review=review)
    if request.method == 'POST':  # check post
        form = CommentForm(request.POST)
        if form.is_valid():

            text = form.cleaned_data['text']
            # return HttpResponse(comment.text)
            user = request.user
            comment = review.comment_set.create(text=text,user=user)
            comment.save()
            return HttpResponseRedirect(url)
    template = 'myalbums/song_detail.html'
    context = {'form': form}
    return render(request, template, context)

def show_notification(request, notification_id):
    n = Notification.objects.get(id=notification_id)
    return render (request, 'myalbums/notification.html', {'notification':n})

def show_notification(request):
    object_list = Notification.objects.all()
    n = Notification.objects.last()
    return render (request, 'myalbums/notification.html', {'notification': n, 'object_list':object_list})

def delete_notification(request, notification_id):
    n = Notification.objects.get(id=notification_id)
    n.viewed = True
    n.save()

    return HttpResponseRedirect('myalbums/notification.html', {'notification':n})
