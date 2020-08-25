from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, DeleteView, ListView
from .models import *
# from utils.song_utils import generate_key
# from .forms import *
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

class ArtistDetailView(DetailView):
    model = Artist
