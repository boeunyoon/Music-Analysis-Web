import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


import datetime
import base64
from urllib.parse import urlencode

#Spotify 권한
cid = 'd67a16df3cd94badb6475cad9054a4b4'
secret = '89e6735383354d4db6a119d3d00cbbbb'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)


class Spotify_audio_features:
    def __init__(self):
        # initial setting
        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def get_features(self, song):
        # get track id information
        track_info = self.sp.search(q=song, type='track', market='JP')
        track_id = track_info["tracks"]["items"][0]["id"]

        # get audio_feature
        features = self.sp.audio_features(tracks=[track_id])
        acousticness = features[0]["acousticness"]
        danceability = features[0]["danceability"]
        energy = features[0]["energy"]
        liveness = features[0]["liveness"]
        loudness = features[0]["loudness"]
        valence = features[0]["valence"]
        mode = features[0]["mode"]

        result = {"acousticness" : acousticness,
                    "danceability" : danceability,
                    "energy" : energy,
                    "liveness" : liveness,
                    "loudness" : loudness,
                    "valence" : valence,
                    "mode" : mode}
        
        return result
    def get_top(self):
        self.sp.current_user_top_tracks(20, 0, 'medium_term')
        

def get_top_100(date):

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    #빌보드 Top 100 데이터 가져오기
    #날짜 타입은 YYYY-MM-DD
    url = 'https://www.billboard.com/charts/hot-100/'

    response = requests.get(f'{url}{date}')
    response_html = response.text


    data = BeautifulSoup(response_html, 'html.parser')
    class_data = 'c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only'
    top_songs = data.find_all(name = 'h3', id = 'title-of-a-story', class_ = class_data)
    top_100 = [song.get_text().strip() for song in top_songs]

    #top1은 top100과 클래스가 다름
    top_1_class_data = 'c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet'
    top_1_song = data.find_all(name = 'h3', id = 'title-of-a-story', class_ = top_1_class_data)
    top_1 = [song.get_text().strip() for song in top_1_song]

    top_100.insert(0, top_1[0])
    
    #rank_for_song = int(input('Which song do you want to know at ' + date + ' rank? at: ')) - 1
    #song_title = top_100[rank_for_song]
    #saf = Spotify_audio_features()
    #feat = saf.get_features(song_title)

    return top_100

def get_song_status(songtitle):
    saf = Spotify_audio_features()
    feat = saf.get_features(songtitle)

    return feat

