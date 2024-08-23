from django.urls import path
from .views import SongSearchView

urlpatterns = [
    path('search-song/', SongSearchView.as_view(), name='search_song'),
]
