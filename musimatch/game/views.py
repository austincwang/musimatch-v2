from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import random
import requests
from io import BytesIO
from pygame import mixer
import time
import pygame.mixer
import nltk

nltk.download('words')
from nltk.corpus import words

pygame.mixer.init()

client_id = settings.CLIENT_ID
client_secret = settings.CLIENT_SECRET
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
word_list = words.words()


# Create your views here.
def join_game(request):
    context = {}
    list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    context['things'] = list
    return render(request, 'join_game.html', context)


def download_song_preview(track_id):
    track_info = sp.track(track_id)
    preview_url = track_info.get('preview_url')

    if not preview_url:
        return None

    try:
        response = requests.get(preview_url)
        audio_data = BytesIO(response.content)
        return audio_data
    except requests.exceptions.RequestException as e:
        print(f"Error downloading audio preview: {e}")
        return None


def play_song_preview(track_id):
    audio_data = download_song_preview(track_id)

    if audio_data is None:
        return HttpResponse("Sorry, the audio preview is not available.")

    pygame.mixer.music.load(audio_data)
    pygame.mixer.music.play()
    time.sleep(2)
    pygame.mixer.music.stop()

    # Wait for the song to finish playing
    while pygame.mixer.music.get_busy():
        continue

    # Stop the song
    pygame.mixer.music.stop()


def play_random_song(request):
    random_q = random.choice(word_list)
 
    results = sp.search(q=random_q, type='track', limit=50) 
    tracks_with_previews = [track for track in results['tracks']['items'] if track.get('preview_url')]

    if not tracks_with_previews:
        return HttpResponse("No tracks with audio previews found.") # make it a while loop so something is always found

    # Select a random track from the list
    random_track = random.choice(tracks_with_previews)
    track_name = random_track['name']
    track_artist = random_track['artists'][0]['name']
    track_id = random_track['id']

    print(track_name)
    print(track_artist)

    # Play the song preview
    play_song_preview(track_id)

    message = f"You just heard {track_name}"
    popup_notification_script = f"""
    <script>
        window.location.href = '/';
        alert("{message}");
    </script>
    """
    return HttpResponse(popup_notification_script)


def play_random_song_by_artist(artist):
    results = sp.search(q=f'artist:{artist}', type='track', limit=50)
    tracks_with_previews = [track for track in results['tracks']['items'] if track.get('preview_url')]

    if not tracks_with_previews:
        print("no tracks")
        return HttpResponse("No tracks with audio previews found.") # make it a while loop so something is always found

    # Select a random track from the list
    random_track = random.choice(tracks_with_previews)
    track_name = random_track['name']
    track_artist = random_track['artists'][0]['name']
    track_id = random_track['id']

    print(f"name: {track_name}")
    print(f"artist: {track_artist}")

    # Play the song preview
    play_song_preview(track_id)

    message = f"You just heard {track_name}"
    popup_notification_script = f"""
    <script>
        window.location.href = '/';
        alert("{message}");
    </script>
    """
    return HttpResponse(popup_notification_script)


# # fix
# def play_random_song_by_genre(request, genre):
#     results = sp.search(q=f'genre:"{genre}"', type='track', limit=50)
#     tracks_with_previews = [track for track in results['tracks']['items'] if track.get('preview_url')]

#     if not tracks_with_previews:
#         return HttpResponse("No tracks with audio previews found.")  # change to just an error popup

#     # Select a random track from the list
#     random_track = random.choice(tracks_with_previews)
#     track_name = random_track['name']
#     track_id = random_track['id']

#     # Play the song preview
#     play_song_preview(track_id)

#     message = f"You just heard {track_name}"
#     popup_notification_script = f"""
#     <script>
#         window.location.href = '/';
#         alert("{message}");
#     </script>
#     """
#     return HttpResponse(popup_notification_script)

# search 


def artist_search(request):
    if request.method == 'POST':
        artist = request.POST.get('submission', '') # this is where we modify what happens after submission
        play_random_song_by_artist(artist)
    return render(request, 'artist.html', {'artist': artist})
    #return HttpResponse(artist)

def genre_search(request):
    if request.method == 'POST':
        genre = request.POST.get('submission', '')
    return HttpResponse(genre)

def time_period_search(request):
    if request.method == 'POST':
        time_period = request.POST.get('submission', '')
    return HttpResponse(time_period)


# category
def play_by_artist(request):
    return render(request, 'artist.html')

def play_by_genre(request):
    return render(request, 'genre.html')

def play_by_time_period(request):
    return render(request, 'time_period.html')




# def index(request):
#     if request.method=='POST':
#         artist_uri = request.POST.get('uri')
#         spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=\
#                 '845df6cbf5ee42f4884ebd14605fd17c',client_secret='d59c601d020b4266bc2ab27a95520cb1',))
#         results = spotify.artist_top_tracks(artist_uri)
#         final_result=results['tracks'][:10]
#         return render(request,'base.html',{"results":final_result})
#     else:
# # for track in results['tracks'][:10]:
# #     print('track    : ' + track['name'])
# #     print('audio    : ' + track['preview_url'])
# #     print('cover art: ' + track['album']['images'][0]['url'])
# #     print()
#       return render(request,'base.html',)


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