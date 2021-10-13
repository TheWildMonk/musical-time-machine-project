# Import necessary libraries
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from spotipy.client import Spotify

# Import credentials
load_dotenv("/Volumes/Workstation/Learning Center/Data Science/"
            "100 Days of Code - Complete Python Pro Bootcamp 2021/Projects/@CREDENTIALS/.env")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = "https://example.com"

# Spotipy set up for Spotify authorization
auth_manager = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET,
                            redirect_uri=REDIRECT_URI, scope="playlist-modify-private")
spotify_auth = Spotify(auth_manager=auth_manager)
user_id = spotify_auth.me()["id"]

# User input for date
user_input_date = input("Which year do you want to travel to? Type the date [Date Format: YYYY-MM-DD]}: ")
date = dt.strptime(user_input_date, "%Y-%m-%d").date()

# Create playlist
playlist = spotify_auth.user_playlist_create(user=user_id, name=f"{date} Billboard 100",
                                             public=False)
playlist_id = playlist["id"]

# Billboard site's HTML
response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}")
response.raise_for_status()
billboard_site = response.text

# Retrieve song titles for user mentioned date
soup = BeautifulSoup(billboard_site, "html.parser")
raw_song_titles = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
song_titles = [titles.getText() for titles in raw_song_titles]

# Extracting Spotify URI
tracks = []
for track in song_titles:
    try:
        result = spotify_auth.search(q=f"name: {track} "
                                       f"year: {date.year}")["tracks"]["items"][0]["uri"]
        tracks.append(result)
    except IndexError:
        pass

# Add tracks to the playlist
spotify_auth.playlist_add_items(playlist_id=playlist_id, items=tracks, position=None)
