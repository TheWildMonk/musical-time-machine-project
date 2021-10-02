# Import necessary libraries
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Import credentials
load_dotenv("/Volumes/Workstation/Learning Center/Data Science/"
            "100 Days of Code - Complete Python Pro Bootcamp 2021/Projects/.env")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")


# User input
date = input("Which year do you want to travel to? Type the date [Date Format: YYYY-MM-DD]}: ")

# Billboard site's HTML
response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}")
response.raise_for_status()
billboard_site = response.text

# Retrieve song titles for user mentioned date
soup = BeautifulSoup(billboard_site, "html.parser")
raw_song_titles = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
song_titles = [titles.getText() for titles in raw_song_titles]
