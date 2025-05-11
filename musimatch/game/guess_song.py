import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import time
from pygame import mixer
import requests
from io import BytesIO
import nltk
from django.conf import settings

nltk.download('words')
from nltk.corpus import words
word_list = words.words()

# Spotify API credentials
client_id = settings.CLIENT_ID
client_secret = settings.CLIENT_SECRET

# Set up Spotify client credentials
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def download_song_preview(track_id):
    # Get the track's preview URL
    track_info = sp.track(track_id)
    preview_url = track_info.get('preview_url')

    if not preview_url:
        print(f"Sorry, the audio preview is not available for the track {track_info['name']}")
        return None

    # Download the audio preview
    try:
        response = requests.get(preview_url)
        audio_data = BytesIO(response.content)
        return audio_data
    except requests.exceptions.RequestException as e:
        print(f"Error downloading audio preview: {e}")
        return None

def play_song_preview(track_id):
    # Download the audio preview
    audio_data = download_song_preview(track_id)

    if audio_data is None:
        return

    # Initialize the mixer
    mixer.init()
    mixer.music.load(audio_data)
    mixer.music.play()

    # Wait for the song to finish playing
    time.sleep(5) 

    # Stop the song
    mixer.music.stop()

def play_game():
    # # Get a list of popular tracks
    # results = sp.playlist_tracks('37i9dQZEVXbMDoHDwVN2tF')  # This is the ID of Spotify's "Today's Top Hits" playlist
    # tracks = results['items']

    # # Select a random track from the playlist
    # random_track = random.choice(tracks)
    # track_name = random_track['track']['name']
    # track_id = random_track['track']['id']


    while True:
        random_q = random.choice(word_list)
        # Get a random list of tracks with audio previews
        results = sp.search(q=random_q, type='track', limit=50)
        tracks_with_previews = [track for track in results['tracks']['items'] if track.get('preview_url')]

        if not tracks_with_previews:
            print("No tracks with audio previews found. Exiting.")
            exit()
        
        # Shuffle the list of tracks (can remove)
        random.shuffle(tracks_with_previews)

        # Select a random track from the list
        random_track = random.choice(tracks_with_previews)
        track_name = random_track['name']
        track_id = random_track['id']

        print("Guess the song!")
        print(f"Song: {track_name}")
        
        # Play the song preview
        play_song_preview(track_id)

        # Get user's guess
        user_guess = input("Your guess: ").strip()

        # Check if the guess is correct
        if user_guess.lower() == track_name.lower():
            print(f"{track_name} is correct!")
            break
        else:
            print(f"The correct answer was: {track_name}")
            break

# Main loop for the game
play = False
while play:
    play_game()

    # Ask if the user wants to play again
    while True:
        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again == 'n':
            print("Thanks for playing!")
            exit()  # Exiting the script if the user chooses not to play again
        elif play_again == 'y':
            break  # Break the inner loop and play again
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def search_random_track(artist):
    # Search for the artist
    results = sp.search(q='artist:' + artist, type='artist', limit=1)
    if len(results['artists']['items']) == 0:
        print("No artist found with the name", artist)
        return

    artist_id = results['artists']['items'][0]['id']

    # Get the top tracks for the artist
    top_tracks = sp.artist_top_tracks(artist_id)

    if len(top_tracks['tracks']) == 0:
        print("No tracks found for the artist", artist)
        return

    # Select a random track from the top tracks
    random_track = random.choice(top_tracks['tracks'])

    return random_track

# Example usage
artist_name = input("Enter the name of an artist: ")
track = search_random_track(artist_name)
if track:
    print("Random track by", artist_name, ":", track['name'])
    print("Preview URL:", track['preview_url'])