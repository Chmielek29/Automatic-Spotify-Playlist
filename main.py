from bs4 import BeautifulSoup
import requests
import spotipy

sp = spotipy.Spotify(
    auth_manager=spotipy.oauth2.SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="dda9911abf554afc8dfceabe163a2312",
        client_secret="512ca1957b7b44c0b590aaf59a046768",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

date = input("Which year do you want to travel to? Type the data in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(URL)
class_name = "u-line-height-125"

soup = BeautifulSoup(response.text, "html.parser")

songs = soup.find_all("h3", id="title-of-a-story", class_=class_name)
songs_list = []

for song in songs:
    song_name = song.getText()
    stripped_song = song_name.strip()
    songs_list.append(stripped_song)

song_uris = []
year = date.split("-")[0]

for track in songs_list:
    result = sp.search(q=f"track:{track} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except:
        print(f"{track} doesn`t exist in Spotify.")

playlist = sp.user_playlist_create(
    user="dawid03298",
    name=date+" Billboard 100",
    public=False
)

add_songs = sp.playlist_add_items(
    playlist_id=playlist["id"],
    items=song_uris,
)
