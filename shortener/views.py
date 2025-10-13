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

# Redirect with click tracking
def redirect_url(request, short_code):
    try:
        url = URL.objects.get(short_code=short_code)

        # Track the click
        from .utils import get_client_ip, get_device_type, get_location
        ip = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        referrer = request.META.get('HTTP_REFERER', '')
        device_type = get_device_type(user_agent)
        location = get_location(ip)

        from .models import URLClick
        URLClick.objects.create(
            url=url,
            ip_address=ip,
            user_agent=user_agent,
            referrer=referrer,
            device_type=device_type,
            country=location.get('country', ''),
            city=location.get('city', '')
        )

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
import uuid
import threading
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from yt_dlp import YoutubeDL
from pytube import YouTube
from .models import DownloadTask
from .consumers import DownloadProgressConsumer

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
                # Fetch available formats using yt-dlp with comprehensive options
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'extract_flat': False,
                    'format_sort': ['res:1080', 'res:720', 'res:480', 'res:360', 'res:240', 'res:144'],
                }
                with YoutubeDL(ydl_opts) as ydl:
                    video_info = ydl.extract_info(video_url, download=False)
                    formats = video_info.get('formats', [])

                # Filter and process formats - include both video and audio formats
                filtered_formats = []
                for fmt in formats:
                    # Include video formats (with height) and audio formats
                    if fmt.get('height') and 144 <= fmt.get('height', 0) <= 1080:
                        # Video format
                        fmt['filesize_mb'] = round(fmt.get('filesize', 0) / (1024 * 1024), 2) if fmt.get('filesize') else 'Unknown'
                        fmt['format_note'] = fmt.get('format_note', f"{fmt.get('height', 'Unknown')}p")
                        fmt['type'] = 'video'
                        filtered_formats.append(fmt)
                    elif fmt.get('acodec') != 'none' and fmt.get('vcodec') == 'none':
                        # Audio-only format
                        fmt['filesize_mb'] = round(fmt.get('filesize', 0) / (1024 * 1024), 2) if fmt.get('filesize') else 'Unknown'
                        fmt['format_note'] = f"Audio {fmt.get('abr', 'Unknown')}kbps"
                        fmt['type'] = 'audio'
                        filtered_formats.append(fmt)

                # Sort by quality (height for video, bitrate for audio)
                filtered_formats.sort(key=lambda x: (
                    0 if x.get('type') == 'video' else 1,  # Videos first
                    x.get('height', 0) if x.get('type') == 'video' else x.get('abr', 0)
                ), reverse=True)

                # Remove duplicates based on format_id
                seen_formats = set()
                unique_formats = []
                for fmt in filtered_formats:
                    if fmt.get('format_id') not in seen_formats:
                        seen_formats.add(fmt.get('format_id'))
                        unique_formats.append(fmt)

                # Fetch thumbnail using pytube
                yt = YouTube(video_url)
                thumbnail_url = yt.thumbnail_url
                video_title = yt.title

                # Add the formats and thumbnail to the context
                context['formats'] = unique_formats[:20]  # Limit to 20 formats
                context['video_url'] = video_url
                context['thumbnail_url'] = thumbnail_url
                context['video_title'] = video_title
            except Exception as e:
                context['error'] = f"Failed to fetch video formats and thumbnail: {str(e)}"

    return render(request, 'youtube.html', context)

def progress_hook(d):
    """Progress hook for yt-dlp to send real-time updates"""
    task_id = getattr(threading.current_thread(), 'task_id', None)
    if not task_id:
        return

    if d['status'] == 'downloading':
        try:
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)

            if total > 0:
                progress = int((downloaded / total) * 100)
            else:
                progress = 0

            # Send progress update via WebSocket
            progress_data = {
                'type': 'progress',
                'progress': progress,
                'speed': d.get('speed', 0),
                'eta': d.get('eta', 0),
                'downloaded': downloaded,
                'total': total,
                'filename': d.get('filename', ''),
            }

            DownloadProgressConsumer.send_progress_update(task_id, progress_data)

        except Exception as e:
            print(f"Progress hook error: {e}")

    elif d['status'] == 'finished':
        progress_data = {
            'type': 'completed',
            'filename': d.get('filename', ''),
            'filesize': d.get('total_bytes', 0),
        }
        DownloadProgressConsumer.send_progress_update(task_id, progress_data)

@csrf_exempt
def start_download(request):
    """Starts the download process and returns task ID"""
    if request.method == 'POST':
        format_id = request.POST.get('format_id')
        video_url = request.POST.get('video_url')

        if video_url and format_id:
            # Create download task
            task_id = str(uuid.uuid4())
            task = DownloadTask.objects.create(
                task_id=task_id,
                video_url=video_url,
                format_id=format_id,
                status='pending'
            )

            # Start download in background thread
            thread = threading.Thread(target=download_video_async, args=(task_id,))
            thread.daemon = True
            setattr(thread, 'task_id', task_id)  # Set task_id on thread for progress hook
            thread.start()

            return JsonResponse({
                'success': True,
                'task_id': task_id,
                'message': 'Download started'
            })

    return JsonResponse({'success': False, 'error': 'Invalid parameters'})

def download_video_async(task_id):
    """Download video in background thread"""
    try:
        task = DownloadTask.objects.get(task_id=task_id)
        task.status = 'downloading'
        task.save()

        ydl_opts = {
            'format': task.format_id,
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
            'quiet': True,
            'no_warnings': True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(task.video_url, download=True)
            filename = ydl.prepare_filename(info)

        # Update task as completed
        task.status = 'completed'
        task.filename = os.path.basename(filename)
        task.file_size = os.path.getsize(filename) if os.path.exists(filename) else 0
        task.save()

    except Exception as e:
        task.status = 'failed'
        task.error_message = str(e)
        task.save()

        # Send error update
        error_data = {
            'type': 'error',
            'error': str(e)
        }
        DownloadProgressConsumer.send_progress_update(task_id, error_data)

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

    return HttpResponse("Invalid request parameters.", status=400)