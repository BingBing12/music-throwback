import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from decouple import config

date = input("Enter a date in the format 'yyyy-mm-dd': ")
url = f"https://www.billboard.com/charts/hot-100/{date}/"
CLIENT_ID = config("CLIENT_ID")
CLIENT_SECRET = config("CLIENT_SECRET")

response = requests.get(url)
web_html = response.text

song_title = []

soup = BeautifulSoup(web_html, "html.parser")
song_blocks = soup.select(selector=".o-chart-results-list__item #title-of-a-story")

for song in song_blocks:
    song_title.append(song.text)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    ))
user_id = sp.current_user()["id"]
song_uris = []
year = date.split("-")[0]
for song in song_title:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

