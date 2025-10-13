# =================================================================================
from django.contrib import admin
from django.urls import path
from shortener.views import ShortenURLView, redirect_url, index, about, youtube, base, start_download, download_thumbnail, dashboard

urlpatterns = [
    # URL Shortener routes
    path('', index, name='index'),
    path('about', about, name='about'),
    path('base', base, name='base'),
    path('dashboard/', dashboard, name='dashboard'),
      # YouTube downloader routes
      path('youtube/', youtube, name='youtube'),
    path('start_download/', start_download, name='start_download'),
    path('download_thumbnail/', download_thumbnail, name='download_thumbnail'),
    # API routes
    path('shorten/', ShortenURLView.as_view(), name='shorten_url'),  # API for shortening
    path('<str:short_code>/', redirect_url, name='redirect_url'),  # Redirect short URL


]
