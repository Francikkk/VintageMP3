from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
import requests
import datetime
import spotipy

SPOTY_CLIENT_ID = ""
SPOTY_CLIENT_SECRET = ""
now = datetime.datetime.now()
today = now.strftime("%Y-%m-%d")
print(f"Today's date is {today}")
song_names = []
song_uris = []

def check_input (date):
    if (date[0] < 1920) or (date[0] > int(now.year)) or (date[0] == int(now.year) and date[1] > int(now.month)) or (date[0] == int(now.year) and date[1] == int(now.month) and date[2] > int(now.day)):
        return False
    else:
        return True
#--------------------------------- INPUT DATE ---------------------------------#
while True:
    date_in = input("Which date do you want to travel to? Type the date in this format YYYY-MM-DD:\n")
    try:
        date_in_tpl = (int(date_in.split("-")[0]), int(date_in.split("-")[1]), int(date_in.split("-")[2]))
    except IndexError:
        print("Please, enter a valid date.\n")
        continue
    except ValueError:
        print("Please, enter a valid date.\n")
        continue
    if date_in_tpl != None and check_input(date_in_tpl):
        year_in = int(date_in.split("-")[0])
        break
    else:
        print("Please, enter a valid date.\n")
#--------------------------------- GET SONGS FROM BILLBOARD ---------------------------------#
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date_in}/")
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")
songs = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in songs]
#--------------------------------- AUTHENTICATE SPOTIFY ---------------------------------#
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://www.billboard.com/charts/hot-100/",
        client_id=SPOTY_CLIENT_ID,
        client_secret=SPOTY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username="francik9", 
    )
)
#--------------------------------- FIND SONGS ON SPOTIFY ---------------------------------#
user_id = sp.current_user()["id"]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year_in}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
#--------------------------------- CREATE PLAYLIST ---------------------------------#
playlist = sp.user_playlist_create(user=user_id, name=f"{date_in} Billboard 100", public=False)
pprint(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)



