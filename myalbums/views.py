

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, DeleteView, ListView
from .models import *
# from utils.song_utils import generate_key
from .forms import UserUpdateForm, ProfileUpdateForm
from tinytag import TinyTag

def index(request):
	return render(request,'index.html')

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
def profile (request):
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

    context  = {
         'u_form' : u_form,
         'p_form' : p_form
     }
    return render(request, 'registration/profile.html', context)

class ArtistDetailView(DetailView):
    model = Artist
