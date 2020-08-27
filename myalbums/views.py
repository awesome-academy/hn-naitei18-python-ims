from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, DeleteView, ListView
from .models import Song, Artist, Category, Album, Review, User, Profile
# from utils.song_utils import generate_key
from .forms import UserUpdateForm, ProfileUpdateForm
from .forms import RegisterForm
from tinytag import TinyTag
from django.http import  HttpResponseRedirect

def index(request):
    context = {
        'artists' : Artist.objects.all(),
        'genres': Category.objects.all()[:6],
        'latest_songs': Song.objects.all()[:6]
    }  
    return render(request, "index.html", context)


class CategoryListView(ListView):
    model = Category


class CategoryDetailView(DetailView):
    model = Category


class SongListView(ListView):
    model = Song


class SongDetailView(DetailView):
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
            form.save()
            return redirect('index') 
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


