from django.http import JsonResponse
from django.views import View
from googleapiclient.discovery import build
from .models import GetAPI

def get_youtube_api_key():
    api_instance = GetAPI.objects.first()
    if api_instance:
        return api_instance.api
    return None

def search_youtube(query):
    YOUTUBE_API_KEY = get_youtube_api_key()
    if not YOUTUBE_API_KEY:
        return None, "YouTube API key not found in the database."

    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=1
    )
    response = request.execute()
    video_id = response['items'][0]['id']['videoId']
    video_title = response['items'][0]['snippet']['title']
    return f"https://www.youtube.com/watch?v={video_id}", video_title


class SongSearchView(View):
    def get(self, request):
        song_name = request.GET.get('song', None)
        if not song_name:
            return JsonResponse({"error": "Please provide a song name"}, status=400)

        youtube_link, video_title = search_youtube(song_name)
        if not youtube_link:
            return JsonResponse({"error": video_title}, status=500)  # Handle missing API key or other errors

        return JsonResponse({"title": video_title, "link": youtube_link})
