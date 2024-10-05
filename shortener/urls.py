# =================================================================================
from django.contrib import admin
from django.urls import path
from shortener.views import ShortenURLView, redirect_url, index, about, youtube
from django.urls import path

urlpatterns = [
    # URL Shortener routes
    # path('', index, name='index'),  # URL Shortener home page
    # path('shorten/', ShortenURLView.as_view(), name='shorten_url'),
    # path('<str:short_code>', RedirectURL.as_view(), name='redirect'),  
    # path('about/', about, name='about'),  # About page
    path('', index, name='index'),  # Home page
    path('shorten/', ShortenURLView.as_view(), name='shorten_url'),  # API for shortening
    path('<str:short_code>/', redirect_url, name='redirect_url'),  # Redirect short URL
    path('about', about, name='about'), 


    # YouTube downloader routes
     path('youtube/', youtube, name='youtube'),


]
