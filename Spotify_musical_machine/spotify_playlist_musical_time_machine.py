from pprint import pprint

import requests
from bs4 import BeautifulSoup
date=input("Enter the year you want to travel back to in the format of YYYY-MM-DD eg:2010-12-26\n")
year=date.split("-")[0]
url=f"https://www.billboard.com/charts/hot-100/{date}/"
response=requests.get(url=url)
webpage=response.text

soup=BeautifulSoup(webpage,"html.parser")

song_names=soup.select(".a-font-primary-bold-s")
songs_names_list=[]
singer_names_list=[]
song_names=soup.findAll("h3","a-no-trucate")
for song in song_names:
    name=song.getText().strip()
    songs_names_list.append(name)
singer_names=soup.findAll("span","a-no-trucate")
for singer_name in singer_names:
    name=singer_name.getText().strip()


print(songs_names_list)

import spotipy
from spotipy.oauth2 import SpotifyOAuth #SpotifyOAuth is a separate module to provide authentication as all methods require user authentication
#authentication requires the client id and secret which you can get when you register your app in the developer dashboard of spotify

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private",
                                client_id="e89adcbcf1884752b877a79af812de92",
                                client_secret="9dcd307e12c24222832c493884067141",
                                redirect_uri="http://localhost:8888/callback",#random redirect uri it need not be specific it could have been (https://example.com/)  also
                                show_dialog = True,
                                cache_path = "token.txt"))


user=sp.current_user()["id"]
print(user)
print(f"Here is the url where you can check the top 100 songs for the year {year} {url}")

songs_uri_list=[]
for song in songs_names_list:
    result = sp.search(q=f"track:{song} year:{year} ")
    if(len(result["tracks"]["items"])!=0):
        uri = result["tracks"]["items"][0]["uri"]
        songs_uri_list.append(uri)
playlist=sp.user_playlist_create(user=user,
                                 name=f"Global Top 100 songs of the year {year}",
                                 public=False,
                                 collaborative=False,
                                 description="Time machine")
playlist_id=playlist["id"]

sp.playlist_add_items(playlist_id=playlist_id,items=songs_uri_list,position=None)













