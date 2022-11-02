import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .models import MusicStatus, Date

import datetime
import base64
from urllib.parse import urlencode
import ast
import json
#Spotify 권한
cid = 'd67a16df3cd94badb6475cad9054a4b4'
secret = '89e6735383354d4db6a119d3d00cbbbb'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)


class Spotify_audio_features:
    def __init__(self):
        # initial setting
        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def get_features(self, song, limit = 10):
        # get track id information
        track_info = self.sp.search(q=song, limit=limit, type='track', market='US')
        if track_info["tracks"]["items"] == []:
            return None


        json_length = len(track_info["tracks"]["items"])
        return_data = []

        for i in range(0, json_length):
            track_id = track_info["tracks"]["items"][i]["id"]
            if MusicStatus.objects.filter(track_id=track_id).exists():
                data = MusicStatus.objects.get(track_id=track_id)

                result = {"track_id" : data.track_id,
                            "title" : data.title,
                            "artist" : data.artist,
                            "acousticness" : data.acousticness,
                            "danceability" : data.danceability,
                            "energy" : data.energy,
                            "liveness" : data.liveness,
                            "loudness" : data.loudness,
                            "valence" : data.valence,
                            "mode" : data.mode,
                            "speechiness": data.speechiness,
                            "instrumentalness": data.instrumentalness,
                            "tempo": data.tempo,
                            "duration_ms": data.duration_ms,
                            "popularity": popularity
                            }
                return_data.append(result)
            else:
                title = track_info["tracks"]["items"][i]["name"]
                artist = track_info["tracks"]["items"][i]["artists"][0]["name"]
                # get audio_feature
                features = self.sp.audio_features(tracks=[track_id])
                acousticness = features[0]["acousticness"]
                danceability = features[0]["danceability"]
                energy = features[0]["energy"]
                liveness = features[0]["liveness"]
                loudness = features[0]["loudness"]
                valence = features[0]["valence"]
                mode = features[0]["mode"]
                speechiness = features[0]["speechiness"]
                instrumentalness = features[0]["instrumentalness"]
                tempo = features[0]["tempo"]
                duration_ms = features[0]["duration_ms"]
                popularity = track_info["tracks"]["items"][i]["popularity"]
                result = {"track_id" : track_id,
                            "title": title,
                            "artist": artist,
                            "acousticness" : acousticness,
                            "danceability" : danceability,
                            "energy" : energy,
                            "liveness" : liveness,
                            "loudness" : loudness,
                            "valence" : valence,
                            "mode" : mode,
                            "speechiness": speechiness,
                            "instrumentalness": instrumentalness,
                            "tempo": tempo,
                            "duration_ms": duration_ms,
                            "popularity": popularity
                            }
                music_status = MusicStatus(track_id=track_id, title=title, artist=artist, acousticness=acousticness,
                danceability=danceability, energy=energy, liveness=liveness, loudness=loudness, valence=valence, mode=mode,
                speechiness=speechiness, instrumentalness=instrumentalness, tempo=tempo, duration_ms=duration_ms, 
                popularity=popularity)
                music_status.save()
                return_data.append(result)
        
        return return_data
    def get_top(self):
        self.sp.current_user_top_tracks(20, 0, 'medium_term')
        

def get_top_100(date):
    if Date.objects.filter(date=date).exists():
        data = Date.objects.get(date=date)
        
        result = {
            "date": data.date,
            "rank": data.rank
        }

        return result
    else:      
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
        result = {
            "date": date,
            "rank": top_100
        }

        top_100_with_date = Date(date=date, rank=top_100)
        top_100_with_date.save()

        return result

def get_avg_status_for_top_100(date):
    data = Date.objects.get(date=date)
    rank = ast.literal_eval(data.rank)
    saf = Spotify_audio_features()

    acousticness = 0
    danceability = 0
    energy = 0
    liveness = 0
    loudness = 0
    valence = 0
    mode = 0

    for i in range(0, 100):
        searched_data = saf.get_features(rank[i], limit=1)
        acousticness += searched_data[0]["acousticness"]
        danceability += searched_data[0]["danceability"]
        energy += searched_data[0]["energy"]
        liveness += searched_data[0]["liveness"]
        loudness += searched_data[0]["loudness"]
        valence += searched_data[0]["valence"]
        mode += searched_data[0]["mode"]
        print(searched_data[0]["title"])
    
    avg_acousticness = acousticness/100
    avg_danceability = danceability/100
    avg_energy = energy/100
    avg_liveness = liveness/100
    avg_loudness = loudness/100
    avg_valence = valence/100
    avg_mode = mode/100
    print("aco: ", avg_acousticness, "dance: ", avg_danceability, "energy: ", avg_energy)
    

def get_song_status(songtitle):
    saf = Spotify_audio_features()
    feat = saf.get_features(songtitle)

    return feat

