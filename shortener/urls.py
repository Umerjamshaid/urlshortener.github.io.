# =================================================================================
from django.contrib import admin
from django.urls import path
from shortener.views import ShortenURLView, redirect_url, index, about, youtube, base
from django.urls import path

urlpatterns = [
    # URL Shortener routes
    path('', index, name='index'),  
    path('about', about, name='about'), 
    path('base', base, name='base'),
      # YouTube downloader routes
     path('youtube/', youtube, name='youtube'),
    path('shorten/', ShortenURLView.as_view(), name='shorten_url'),  # API for shortening
    path('<str:short_code>/', redirect_url, name='redirect_url'),  # Redirect short URL


]
