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

# def youtube(request):
#     if request.method == 'POST':
#         link = request.POST['link']
#         resolution = request.POST.get('resolution')  # Get the selected resolution from the form

#         try:
#             # Set options for the downloader
#             ydl_opts = {
#                 'format': f'best[height={resolution}]' if resolution else 'best',
#                 'outtmpl': '%(title)s.%(ext)s',  # Output file name
#             }

#             with YoutubeDL(ydl_opts) as ydl:
#                 # Fetch video information
#                 info = ydl.extract_info(link, download=True)
#                 title = info.get('title', None)
#                 message = f"Downloaded {title} in {resolution or 'best'} resolution."

#             return render(request, 'youtube.html', {'link': link, 'message': message})

#         except Exception as e:
#             return render(request, 'youtube.html', {'error': str(e)})
    
#     return render(request, 'youtube.html')


# Path where the video will be saved
DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def youtube(request):
    context = {}
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        
        if video_url:
            # Use yt-dlp to fetch available formats
            ydl_opts = {'listformats': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                formats = ydl.extract_info(video_url, download=False)['formats']
            
            # Filter formats to only include those between 144p and 720p, check if 'height' exists
            filtered_formats = [fmt for fmt in formats if fmt.get('height') and 144 <= fmt['height'] <= 720]
            
            context['formats'] = filtered_formats
            context['video_url'] = video_url
    
    return render(request, 'youtube.html', context)

def download_video(request):
    if request.method == 'POST':
        format_id = request.POST.get('format_id')
        video_url = request.POST.get('video_url')

        if video_url and format_id:
            ydl_opts = {
                'format': format_id,
                'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            
            return HttpResponse(f"Video downloaded successfully in {format_id} format.")
    
    return HttpResponse("Failed to download the video.")