import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .models import MusicStatus, Top100ByDate, AlbumImage

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

    def get_album_image(self, song, limit=10, track_info=None):
        #get_features 함수에서 접근하는 것이 아닐 경우 직접 이미지 데이터를 가져온다.

        if track_info is None:
            track_info = self.sp.search(q=song, limit=limit, type='track', market='US')

        if track_info["tracks"]["items"] == []:
            return None
        
        json_length = len(track_info["tracks"]["items"])
        return_data = []

        for i in range(0, json_length):
            track_id = track_info["tracks"]["items"][i]["id"]
            if AlbumImage.objects.filter(track_id=track_id).exists():
                data = AlbumImage.objects.get(track_id=track_id)

                result = {"track_id" : data.track_id,
                        "title" : data.title,
                        "artist" : data.artist,
                        "images":[
                            {
                            "height":640,
                            "url":data.img640,
                            "width":640
                            },
                            {
                            "height":300,
                            "url":data.img300,
                            "width":300
                            },
                            {
                            "height":64,
                            "url":data.img64,
                            "width":64
                            }
                        ]
                }
                return_data.append(result)
            else:
                title = track_info["tracks"]["items"][i]["name"]
                artist = track_info["tracks"]["items"][i]["artists"][0]["name"]
                img640 = track_info["tracks"]["items"][i]["album"]["images"][0]["url"]
                img300 = track_info["tracks"]["items"][i]["album"]["images"][1]["url"]
                img64 = track_info["tracks"]["items"][i]["album"]["images"][2]["url"]

                result = {"track_id" : track_id,
                        "title" : title,
                        "artist" : artist,
                        "images":[
                            {
                            "height":640,
                            "url":img640,
                            "width":640
                            },
                            {
                            "height":300,
                            "url":img300,
                            "width":300
                            },
                            {
                            "height":64,
                            "url":img64,
                            "width":64
                            }
                        ]
                }
                album_image = AlbumImage(track_id=track_id, title=title, artist=artist,
                                        img640=img640, img300=img300, img64=img64)
                album_image.save()
                return_data.append(result)
        return return_data


    def get_features(self, song, limit=10):
        # get track id information
        track_info = self.sp.search(q=song, limit=limit, type='track', market='US')
        if track_info["tracks"]["items"] == []:
            #특수문자 검사
            song = str(song)
            song = song.replace('*', 'i')
            track_info = self.sp.search(q=song, type='track', market='US')

            #재검사 이후에도 검색 결과가 없으면 None 반환
            if track_info["tracks"]["items"] == []:
                return None


        json_length = len(track_info["tracks"]["items"])
        return_data = []

        for i in range(0, json_length):
            track_id = track_info["tracks"]["items"][i]["id"]
        

            if AlbumImage.objects.filter(track_id=track_id).exists():
                img_data = AlbumImage.objects.get(track_id=track_id)
                img640 = img_data.img640
                img300 = img_data.img300
                img64 = img_data.img64
            else:
                img_data = self.get_album_image(song=song, limit=limit, track_info=track_info)
                img640 = img_data[i]["images"][0]
                img300 = img_data[i]["images"][1]
                img64 = img_data[i]["images"][2]

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
                            "popularity": data.popularity,
                            "images":[
                                    {
                                    "height":640,
                                    "url":img640,
                                    "width":640
                                    },
                                    {
                                    "height":300,
                                    "url":img300,
                                    "width":300
                                    },
                                    {
                                    "height":64,
                                    "url":img64,
                                    "width":64
                                    }
                                ]
                            }
                return_data.append(result)
            else:
                title = track_info["tracks"]["items"][i]["name"]
                artist = track_info["tracks"]["items"][i]["artists"][0]["name"]
                # get audio_feature
                features = self.sp.audio_features(tracks=[track_id])
                if features[0] == None:
                    acousticness = None
                    danceability = None
                    energy = None
                    liveness = None
                    loudness = None
                    valence = None
                    mode = None
                    speechiness = None
                    instrumentalness = None
                    tempo = None
                    duration_ms = None
                    popularity = None
                else:
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
                            "popularity": popularity,
                            "images":[
                                    {
                                    "height":640,
                                    "url":img640,
                                    "width":640
                                    },
                                    {
                                    "height":300,
                                    "url":img300,
                                    "width":300
                                    },
                                    {
                                    "height":64,
                                    "url":img64,
                                    "width":64
                                    }
                                ]
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
    if Top100ByDate.objects.filter(date=date).exists():
        data = Top100ByDate.objects.get(date=date)
        
        result = {
            "date": data.date,
            "rank": data.rank,
            "averge_status": {
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
                "popularity": data.popularity
            }
        }

        return result
    else:      
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

        #평균 스탯을 계산한다.
        saf = Spotify_audio_features()
        acousticness = 0
        danceability = 0
        energy = 0
        liveness = 0
        loudness = 0
        valence = 0
        mode = 0
        speechiness = 0
        instrumentalness = 0
        tempo = 0
        duration_ms = 0
        popularity = 0

        rank_amount = 100

        for i in range(0, 100):
            searched_data = saf.get_features(top_100[i], limit=1)
            print(searched_data)
            if searched_data[0]["acousticness"] == None:
                rank_amount -= 1
                continue
            acousticness += searched_data[0]["acousticness"]
            danceability += searched_data[0]["danceability"]
            energy += searched_data[0]["energy"]
            liveness += searched_data[0]["liveness"]
            loudness += searched_data[0]["loudness"]
            valence += searched_data[0]["valence"]
            mode += searched_data[0]["mode"]
            speechiness += searched_data[0]["speechiness"]
            instrumentalness += searched_data[0]["instrumentalness"]
            tempo += searched_data[0]["tempo"]
            duration_ms += searched_data[0]["duration_ms"]
            popularity += searched_data[0]["popularity"]

        print(rank_amount)
        acousticness /= rank_amount
        danceability /= rank_amount
        energy /= rank_amount
        liveness /= rank_amount
        loudness /= rank_amount
        valence /= rank_amount
        mode /= rank_amount
        speechiness /= rank_amount
        instrumentalness /= rank_amount
        tempo /= rank_amount
        duration_ms = round(duration_ms/rank_amount)
        popularity = round(popularity/rank_amount)
        
        result = {
            "date": date,
            "rank": top_100,
            "averge_status": {
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
            
        }

        top_100_by_date = Top100ByDate(date=date, rank=top_100, acousticness=acousticness, danceability=danceability, 
                                        energy=energy, liveness=liveness, loudness=loudness, valence=valence, mode=mode,
                                        speechiness=speechiness, instrumentalness=instrumentalness, tempo=tempo, 
                                        duration_ms=duration_ms, popularity=popularity)
        top_100_by_date.save()

        return result

def data_mining(date):
    date_to_int = date.split(sep='-')
    date_to_int = list(map(int, date_to_int))
    saf = Spotify_audio_features()

    while date!="2022-10-08":
        print(date)
        get_top_100(date)
        if date_to_int[0]%4 == 0 and date_to_int[1] == 2:
            if date_to_int[2] == 29:
                date_to_int[2] = 0
                date_to_int[1] += 1
            date_to_int[2] = date_to_int[2] + 1
        elif date_to_int[1] == 2 and date_to_int[2] == 28:
            date_to_int[2] = 1
            date_to_int[1] += 1
        elif date_to_int[2] == 30 and (date_to_int[1] == 4 or date_to_int[1] == 6
                                or date_to_int[1] == 9 or date_to_int[1] == 11):
            date_to_int[2] = 1
            date_to_int[1] += 1
        elif date_to_int[2] == 31:
            date_to_int[2] = 1
            date_to_int[1] += 1
        else:
            date_to_int[2] = date_to_int[2] + 1

        if date_to_int[1] == 13:
            date_to_int[1] = 1
            date_to_int[0] += 1

        year = str(date_to_int[0])
        month = str(date_to_int[1])
        day = str(date_to_int[2])
        if len(month) == 1:
            month = "0" + month
        if len(day) == 1:
            day = "0" + day 

        date = year + "-" + month + "-" + day
        


# 쓰지 않는 함수
def get_avg_status_for_top_100(date):
    
    data = Top100ByDate.objects.get(date=date)
    rank = ast.literal_eval(data.rank)
    saf = Spotify_audio_features()

    acousticness = 0
    danceability = 0
    energy = 0
    liveness = 0
    loudness = 0
    valence = 0
    mode = 0
    speechiness = 0
    instrumentalness = 0
    tempo = 0
    duration_ms = 0
    popularity = 0

    for i in range(0, 100):
        searched_data = saf.get_features(rank[i], limit=1)
        acousticness += searched_data[0]["acousticness"]
        danceability += searched_data[0]["danceability"]
        energy += searched_data[0]["energy"]
        liveness += searched_data[0]["liveness"]
        loudness += searched_data[0]["loudness"]
        valence += searched_data[0]["valence"]
        mode += searched_data[0]["mode"]
        speechiness += searched_data[0]["speechiness"]
        instrumentalness += searched_data[0]["instrumentalness"]
        tempo += searched_data[0]["tempo"]
        duration_ms += searched_data[0]["duration_ms"]
        popularity += searched_data[0]["popularity"]
    
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

