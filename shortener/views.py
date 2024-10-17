# ===============================this is the main code ===========================
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import URL
from .serializers import URLSerializer
from django.shortcuts import redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from rest_framework import status  
from .models import URL
from .serializers import URLSerializer
import random
import string
# ======================yt imports=============================
from django.shortcuts import render
import os
import yt_dlp
from django.http import HttpResponse
from django.shortcuts import render
from pytube import YouTube



# ==========================================Generate short code==============================
def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

#========================================= API View for shortening URLs==============================
class ShortenURLView(APIView):
    def post(self, request):
        serializer = URLSerializer(data=request.data)
        if serializer.is_valid():
            short_code = generate_short_code()
            url = serializer.save(short_code=short_code)
            return Response({"short_url": request.build_absolute_uri(f'/{url.short_code}/')}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Redirect 
def redirect_url(request, short_code):
    try:
        url = URL.objects.get(short_code=short_code)
        return redirect(url.original_url)
    except URL.DoesNotExist:
        return render(request, '404.html', status=404)

def index(request):
    if request.method == 'POST':
        original_url = request.POST.get('url')
        short_code = generate_short_code()
        url = URL.objects.create(original_url=original_url, short_code=short_code)
        return render(request, 'index.html', {'short_url': request.build_absolute_uri(f'/{url.short_code}/')})
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')
def base(request):
    return render(request, 'base.html')

# ============================youtube video downloader====================================== 
# import os
# from django.shortcuts import render, HttpResponse
# from yt_dlp import YoutubeDL
# from pytube import YouTube

# # Path where the video will be saved
# DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')

# if not os.path.exists(DOWNLOAD_DIR):
#     os.makedirs(DOWNLOAD_DIR)

# # YouTube video downloader view
# def youtube(request):
#     context = {}
#     if request.method == 'POST':
#         video_url = request.POST.get('video_url')

#         if video_url:
#             try:
#                 # Use yt-dlp to fetch available formats
#                 ydl_opts = {'listformats': True}
#                 with YoutubeDL(ydl_opts) as ydl:
#                     formats = ydl.extract_info(video_url, download=False)['formats']

#                 # Filter formats to only include those between 144p and 720p
#                 filtered_formats = [fmt for fmt in formats if fmt.get('height') and 144 <= fmt['height'] <= 720]

#                 if not filtered_formats:
#                     context['error'] = 'No suitable formats found for this video.'

#                 context['formats'] = filtered_formats
#                 context['video_url'] = video_url

#             except Exception as e:
#                 context['error'] = f"Error fetching video formats: {str(e)}"

#     return render(request, 'youtube.html', context)

# # Video download view
# def download_video(request):
#     if request.method == 'POST':
#         format_id = request.POST.get('format_id')
#         video_url = request.POST.get('video_url')

#         if video_url and format_id:
#             try:
#                 ydl_opts = {
#                     'format': format_id,
#                     'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
#                 }
#                 with YoutubeDL(ydl_opts) as ydl:
#                     ydl.download([video_url])

#                 return HttpResponse(f"Video downloaded successfully in {format_id} format.")
#             except Exception as e:
#                 return HttpResponse(f"Error downloading video: {str(e)}")

#     return HttpResponse("Failed to download the video.")

# # ============================Thumbnail-downloader===========================================

# def youtube_thumbnail(request):
#     if request.method == 'POST':
#         url = request.POST.get('url')

#         if url:
#             try:
#                 # Get the thumbnail URL from the YouTube video
#                 yt = YouTube(url)
#                 thumbnail_url = yt.thumbnail_url
#                 return render(request, 'result.html', {'thumbnail_url': thumbnail_url})
#             except Exception as e:
#                 # Pass the error message to the template if there's an issue
#                 return render(request, 'youtube.html', {'error': str(e)})

#     # Default rendering of the form page (youtube.html)
#     return render(request, 'youtube.html')


import os
import requests
from django.http import HttpResponse
from django.shortcuts import render
from yt_dlp import YoutubeDL
from pytube import YouTube

# Define download directory
DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def youtube(request):
    """Handles YouTube video download options and fetches thumbnail."""
    context = {}
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        
        if video_url:
            try:
                # Fetch available formats using yt-dlp
                ydl_opts = {'listformats': True}
                with YoutubeDL(ydl_opts) as ydl:
                    video_info = ydl.extract_info(video_url, download=False)
                    formats = video_info['formats']
                
                # Filter formats between 144p and 720p
                filtered_formats = [fmt for fmt in formats if fmt.get('height') and 144 <= fmt['height'] <= 720]

                # Fetch thumbnail using pytube
                yt = YouTube(video_url)
                thumbnail_url = yt.thumbnail_url

                # Add the formats and thumbnail to the context
                context['formats'] = filtered_formats
                context['video_url'] = video_url
                context['thumbnail_url'] = thumbnail_url
            except Exception as e:
                context['error'] = f"Failed to fetch video formats and thumbnail: {str(e)}"
    
    return render(request, 'youtube.html', context)

def download_video(request):
    """Downloads the selected YouTube video in the specified format."""
    if request.method == 'POST':
        format_id = request.POST.get('format_id')
        video_url = request.POST.get('video_url')

        if video_url and format_id:
            try:
                ydl_opts = {
                    'format': format_id,
                    'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
                }
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                
                return HttpResponse(f"Video downloaded successfully in {format_id} format.")
            except Exception as e:
                return HttpResponse(f"Error downloading video: {str(e)}", status=500)
    
    return HttpResponse("Invalid request parameters.", status=400)

def download_thumbnail(request):
    """Downloads the YouTube video thumbnail."""
    if request.method == 'POST':
        thumbnail_url = request.POST.get('thumbnail_url')

        if thumbnail_url:
            try:
                response = requests.get(thumbnail_url)
                thumbnail_path = os.path.join(DOWNLOAD_DIR, 'thumbnail.jpg')
                with open(thumbnail_path, 'wb') as f:
                    f.write(response.content)
                
                return HttpResponse("Thumbnail downloaded successfully.")
            except Exception as e:
                return HttpResponse(f"Error downloading thumbnail: {str(e)}", status=500)
    
    return HttpResponse("Invalid request parameters.",status=400)