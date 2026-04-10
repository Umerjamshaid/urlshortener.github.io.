# =================================================================================
from django.contrib import admin
from django.urls import path
from shortener.views import ShortenURLView, redirect_url, index, about, youtube, base, start_download, download_thumbnail, dashboard, qr_code, url_list

urlpatterns = [
    # URL Shortener routes
    path('', index, name='index'),
    path('about', about, name='about'),
    path('base', base, name='base'),
    path('dashboard/', dashboard, name='dashboard'),
    path('urls/', url_list, name='url_list'),
    # YouTube downloader routes
    path('youtube/', youtube, name='youtube'),
    path('start_download/', start_download, name='start_download'),
    path('download_thumbnail/', download_thumbnail, name='download_thumbnail'),
    # QR code route
    path('qr/<str:short_code>/', qr_code, name='qr_code'),
    # API routes
    path('shorten/', ShortenURLView.as_view(), name='shorten_url'),  # API for shortening
    path('<str:short_code>/', redirect_url, name='redirect_url'),  # Redirect short URL
]
