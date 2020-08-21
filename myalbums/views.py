from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, DeleteView, ListView

# from utils.song_utils import generate_key
# from .forms import *
from tinytag import TinyTag

def index(request):

	return render(request,'index.html')


