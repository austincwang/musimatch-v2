from django.shortcuts import render, redirect
import spotipy
import random
from django.conf import settings

from spotipy.oauth2 import SpotifyClientCredentials

client_id = settings.CLIENT_ID
client_secret = settings.CLIENT_SECRET
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# after creating a game, import game to views.py
# from .artist_games import xxx 

def taylor_swift_guess(request):
    if request.method == "GET":
        results = sp.search(q='Taylor Swift', type='artist', limit=1)
        taylor_id = results['artists']['items'][0]['id']
        taylor_uri = 'spotify:artist:' + taylor_id
        top_tracks = sp.artist_top_tracks(taylor_uri)['tracks']

        selected = random.choice(top_tracks)

        return render(request, 'game/artist_game.html', {
            'track_name': selected['name'],
            'preview_url': selected['preview_url'],
            'album_img': selected['album']['images'][0]['url'],
            'artist_name': selected['artists'][0]['name']
        } )
    
    return redirect('game:artist_search')