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
from pytube import YouTube

class ShortenURLView(APIView):
    def post(self, request):
        serializer = URLSerializer(data=request.data)
        if serializer.is_valid():
            url = serializer.save()  # Save the new URL and generate short_code
            short_url = request.build_absolute_uri(f'/{url.short_code}/')  # Generate the full short URL
            print(f"Shortened URL: {short_url}")  # Debugging line
            return Response({"short_url": short_url}, status=status.HTTP_201_CREATED)
        else:
            print("Serializer errors:", serializer.errors)  # Debugging line
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RedirectURL(APIView):
    def get(self, request, short_code):
        url = get_object_or_404(URL, short_code=short_code)  
        return redirect(url.original_url)  

# # Add this view to render the HTML page
def index(request):
    return render(request, 'shortener/index.html')  # Update with the actual template path

# The view for rendering the About page
def about(request):
    return render(request, 'shortener/about.html')


# Add this view to handle redirects
def redirect_url(request, short_url):
    url_object = get_object_or_404(URL, short_code=short_url)  # Changed 'short_url' to 'short_code'
    return redirect(url_object.original_url)

# Generate a random shortcode
# def generate_short_code():
#     return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

# # API View for shortening URLs
# class ShortenURLView(APIView):
#     def post(self, request):
#         serializer = URLSerializer(data=request.data)
#         if serializer.is_valid():
#             short_code = generate_short_code()
#             url = serializer.save(short_code=short_code)
#             return Response({"short_url": request.build_absolute_uri(f'/{url.short_code}/')}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # Redirect the shortened URL
# def redirect_url(request, short_code):
#     try:
#         url = URL.objects.get(short_code=short_code)
#         return redirect(url.original_url)
#     except URL.DoesNotExist:
#         return render(request, 'shortener/404.html', status=404)

# # Home page for form submission
# def index(request):
#     if request.method == 'POST':
#         original_url = request.POST.get('url')
#         short_code = generate_short_code()
#         url = URL.objects.create(original_url=original_url, short_code=short_code)
#         return render(request, 'shortener/index.html', {'short_url': request.build_absolute_uri(f'/{url.short_code}/')})
#     return render(request, 'shortener/index.html')
# # About page
# def about(request):
#     return render(request, 'shortener/about.html')



# ============================youtube video downloader====================================== 
def youtube(request):
    if request.method == 'POST':
        link = request.POST['link']
        resolution = request.POST.get('resolution')  # Get the selected resolution from the form

        try:
            video = YouTube(link)

            # available streams with video
            streams = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')

            if resolution:
                stream = video.streams.get_by_resolution(resolution)
                if stream:
                    stream.download()
                    message = f"Downloaded {video.title} in {resolution} resolution."
                else:
                    message = f"Resolution {resolution} not available."
            else:

                stream = streams.get_lowest_resolution()
                stream.download()
                message = f"Downloaded {video.title} in the lowest resolution."
            
            return render(request, 'shortener/youtube.html', {'link': link, 'resolutions': streams, 'message': message})

        except Exception as e:
            return render(request, 'shortener/youtube.html', {'error': str(e)})
    
    return render(request, 'shortener/youtube.html')
