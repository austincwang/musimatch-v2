from django.shortcuts import render
from django.http import HttpResponse
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import requests
from io import BytesIO
from pygame import mixer
import time


# Create your views here.
def join_game(request):
    context = {}
    list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    context['things'] = list
    return render(request, 'join_game.html', context)


# ok i need to fix this part
def index(request):
    if request.method=='POST':
        artist_uri = request.POST.get('uri')
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=\
                '845df6cbf5ee42f4884ebd14605fd17c',client_secret='d59c601d020b4266bc2ab27a95520cb1',))
        results = spotify.artist_top_tracks(artist_uri)
        final_result=results['tracks'][:10]
        return render(request,'base.html',{"results":final_result})
    else:
# for track in results['tracks'][:10]:
#     print('track    : ' + track['name'])
#     print('audio    : ' + track['preview_url'])
#     print('cover art: ' + track['album']['images'][0]['url'])
#     print()
      return render(request,'base.html',)


# # Initialize Spotipy client credentials
# client_id = '845df6cbf5ee42f4884ebd14605fd17c'
# client_secret = 'd59c601d020b4266bc2ab27a95520cb1'
# client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# def play_song(request):
#     track_id = 'your_track_id_here'  # You need to pass a valid track ID
#     audio_data = download_song_preview(track_id)
#     if audio_data:
#         play_audio(audio_data)
#         return HttpResponse("Song played successfully!")
#     else:
#         return HttpResponse("Error: Unable to play song.")

# def download_song_preview(track_id):
#     track_info = sp.track(track_id)
#     preview_url = track_info.get('preview_url')
#     if preview_url:
#         try:
#             response = requests.get(preview_url)
#             audio_data = BytesIO(response.content)
#             return audio_data
#         except requests.exceptions.RequestException as e:
#             print(f"Error downloading audio preview: {e}")
#     else:
#         print(f"Sorry, the audio preview is not available for the track {track_info['name']}")
#         return None

# def play_audio(audio_data):
#     mixer.init()
#     mixer.music.load(audio_data)
#     mixer.music.play()
#     time.sleep(5)
#     mixer.music.stop()