# =================================================================================
from django.contrib import admin
from django.urls import path
from shortener.views import ShortenURLView, redirect_url, index, about, youtube, base, download_video, download_thumbnail

urlpatterns = [
    # URL Shortener routes
    path('', index, name='index'),  
    path('about', about, name='about'), 
    path('base', base, name='base'),
      # YouTube downloader routes
      path('youtube/', youtube, name='youtube'),
    path('download/', download_video, name='download_video'),
    path('download_thumbnail/', download_thumbnail, name='download_thumbnail'),
    # API routes 
    path('shorten/', ShortenURLView.as_view(), name='shorten_url'),  # API for shortening
    path('<str:short_code>/', redirect_url, name='redirect_url'),  # Redirect short URL


]
