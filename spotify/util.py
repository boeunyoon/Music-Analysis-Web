import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .models import *
from django.core import serializers
from django.db.models import Q
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import base64
from urllib.parse import urlencode
import ast
import json
#Spotify 권한
cid = '01b9ce28405042deb84a4813e63d557d'
secret = 'd20308c58757497191c1386264672528'
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

                # MusicStatus 모델에 추가된 artist_id를 업데이트한다.
                if data.artist_id is None:
                    artist_id= track_info["tracks"]["items"][i]["artists"][0]["id"]
                    data.artist_id=artist_id
                    data.save()

                result = {"track_id" : data.track_id,
                            "title" : data.title,
                            "artist" : data.artist,
                            "artist_id": data.artist_id,
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
                artist_id= track_info["tracks"]["items"][i]["artists"][0]["id"]
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
                            "artist_id": artist_id,
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

                music_status = MusicStatus(track_id=track_id, title=title, artist=artist, artist_id = artist_id, 
                acousticness=acousticness, danceability=danceability, energy=energy, liveness=liveness, loudness=loudness, 
                valence=valence, mode=mode, speechiness=speechiness, instrumentalness=instrumentalness, tempo=tempo,
                duration_ms=duration_ms, popularity=popularity)
                music_status.save()
                return_data.append(result)
        
        return return_data

    def get_recommendation(self, track_id, artist_id , genre='pop', limit=10):
        recommendations_info = self.sp.recommendations(seed_artist=[artist_id], seed_genres=[genre], 
                                seed_tacks=[track_id], country=["US"] ,limit=limit)
        return_data = []
        for i in range(0, limit):
            result = {
                "title": recommendations_info["tracks"][i]["name"],
                "artist": recommendations_info["tracks"][i]["artists"][0]["name"]
            }
            return_data.append(result)
        
        return return_data
    
    def get_artist_info(self, artist, limit=5):
        artist_info = self.sp.search(q=artist, type='artist',limit=limit, market='US')
        #print(artist_info['artists']['items'][0])
        length = len(artist_info['artists']['items'])

        return_data = []
        for i in range(0, length):
            #아티스트 정보
            artist_id = artist_info['artists']['items'][i]['id']

            if ArtistInfo.objects.filter(artist_id=artist_id).exists():
                data = ArtistInfo.objects.get(artist_id=artist_id)
                artist_name = data.artist
                followers = data.followers
                genres = ast.literal_eval(data.genres)
                artist_img640 = data.img640
                artist_img300 = data.img300
                artist_img64 = data.img64
                popularity = data.popularity
                related_artists = ast.literal_eval(data.related_artists)
            else:
                artist_name = artist_info['artists']['items'][i]['name']
                #print(artist_name)
                followers = artist_info['artists']['items'][i]['followers']['total']
                genres = artist_info['artists']['items'][i]['genres']
                #print(artist_info['artists']['items'][i]['images'])
                if artist_info['artists']['items'][i]['images']:
                    artist_img640 = artist_info['artists']['items'][i]['images'][0]['url']
                    artist_img300 = artist_info['artists']['items'][i]['images'][1]['url']
                    artist_img64 = artist_info['artists']['items'][i]['images'][2]['url']
                popularity = artist_info['artists']['items'][i]['popularity']

                related_artists_info = self.sp.artist_related_artists(artist_id)
                related_artists = []
                for j in range(0, len(related_artists_info['artists'])): #5개보다 적을 경우를 대비
                    if j == 5:
                        #print(len(related_artists))#5개인지 확인
                        break
                    related_artists_id = related_artists_info['artists'][j]['id']
                    related_artists_name = related_artists_info['artists'][j]['name']
                    related_data = {
                        "id": related_artists_id,
                        "name": related_artists_name
                    }
                    related_artists.append(related_data)
                save_artist_info = ArtistInfo(artist_id=artist_id, artist=artist_name, followers=followers,
                                            genres=genres, img640=artist_img640, img300=artist_img300, img64=artist_img64, 
                                            popularity=popularity, related_artists=related_artists)
                save_artist_info.save()
            
            #탑트랙 정보
            if ArtistTopTracks.objects.filter(artist_id=artist_id).exists():
                data = ArtistTopTracks.objects.get(artist_id=artist_id)
                top_tracks = ast.literal_eval(data.top_tracks)
                avg_acousticness = data.acousticness
                avg_danceability = data.danceability
                avg_energy = data.energy
                avg_liveness = data.liveness
                avg_loudness = data.loudness
                avg_valence = data.valence
                avg_mode = data.mode
                avg_speechiness = data.speechiness
                avg_instrumentalness = data.instrumentalness
                avg_tempo = data.tempo
                avg_duration_ms = data.duration_ms
                avg_popularity = data.popularity
            else:
                avg_acousticness = avg_danceability = avg_energy = avg_liveness = avg_loudness = avg_valence = 0
                avg_mode = avg_speechiness = avg_instrumentalness = avg_tempo = avg_duration_ms = avg_popularity = 0
                artist_top_tracks_info = self.sp.artist_top_tracks(artist_id=artist_id, country='US')
                top_tracks = []
                top_tracks_len = len(artist_top_tracks_info['tracks'])
                for j in range(0, top_tracks_len):
                    if j == 5:
                        #print(len(artist_top_tracks_info['tracks']))#5개인지 확인
                        top_tracks_len = 5
                        break
                    track_id = artist_top_tracks_info['tracks'][j]['id']
                    title = artist_top_tracks_info['tracks'][j]['name']
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
                    popularity = artist_top_tracks_info["tracks"][j]["popularity"]
                    if not MusicStatus.objects.filter(track_id=track_id).exists():
                        music_status = MusicStatus(track_id=track_id, title=title, artist=artist_name, artist_id = artist_id, 
                        acousticness=acousticness, danceability=danceability, energy=energy, liveness=liveness, loudness=loudness, 
                        valence=valence, mode=mode, speechiness=speechiness, instrumentalness=instrumentalness, tempo=tempo,
                        duration_ms=duration_ms, popularity=popularity)
                        music_status.save()

                    img640 = artist_top_tracks_info["tracks"][j]['album']["images"][0]['url']
                    img300 = artist_top_tracks_info["tracks"][j]['album']["images"][1]['url']
                    img64 = artist_top_tracks_info["tracks"][j]['album']["images"][2]['url']
                    if not AlbumImage.objects.filter(track_id=track_id).exists():
                        album_image = AlbumImage(track_id=track_id, title=title, artist=artist_name,
                                        img640=img640, img300=img300, img64=img64)
                        album_image.save()

                    avg_acousticness += acousticness
                    avg_danceability += danceability
                    avg_energy += energy
                    avg_liveness += liveness
                    avg_loudness += loudness
                    avg_valence += valence
                    avg_mode += mode
                    avg_speechiness += speechiness
                    avg_instrumentalness += instrumentalness
                    avg_tempo += tempo
                    avg_duration_ms += duration_ms
                    avg_popularity += popularity

                    top_tracks_data = {
                        "track_id" : track_id,
                        "title": title,
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
                    top_tracks.append(top_tracks_data)
                if top_tracks_len > 0:
                    avg_acousticness /= top_tracks_len
                    avg_danceability /= top_tracks_len
                    avg_energy /= top_tracks_len
                    avg_liveness /= top_tracks_len
                    avg_loudness /= top_tracks_len
                    avg_valence /= top_tracks_len
                    avg_mode /= top_tracks_len
                    avg_speechiness /= top_tracks_len
                    avg_instrumentalness /= top_tracks_len
                    avg_tempo /= top_tracks_len
                    avg_duration_ms /= top_tracks_len
                    avg_popularity /= top_tracks_len
                
                save_artist_top_tracks = ArtistTopTracks(artist_id=artist_id, top_tracks=top_tracks, acousticness=avg_acousticness, 
                                                danceability=avg_danceability, energy=avg_energy, liveness=avg_liveness, 
                                                loudness=avg_loudness, valence=avg_valence, mode=avg_mode, speechiness=avg_speechiness, 
                                                instrumentalness=avg_instrumentalness, tempo=avg_tempo, duration_ms=avg_duration_ms, 
                                                popularity=avg_popularity)
                save_artist_top_tracks.save()


            result = {
                "artists": {
                    "id": artist_id,
                    "name": artist_name,
                    "followers": followers,
                    "genres": genres,
                    "popularity": popularity,
                    "images":[
                                {
                                "height":640,
                                "url":artist_img640,
                                "width":640
                                },
                                {
                                "height":300,
                                "url":artist_img300,
                                "width":300
                                },
                                {
                                "height":64,
                                "url":artist_img64,
                                "width":64
                                }
                        ]
                },
                "related_artists": related_artists,
                "top_tracks": {
                    "items": top_tracks,
                    "average_status": {
                        "acousticness" : avg_acousticness,
                        "danceability" : avg_danceability,
                        "energy" : avg_energy,
                        "liveness" : avg_liveness,
                        "loudness" : avg_loudness,
                        "valence" : avg_valence,
                        "mode" : avg_mode,
                        "speechiness": avg_speechiness,
                        "instrumentalness": avg_instrumentalness,
                        "tempo": avg_tempo,
                        "duration_ms": avg_duration_ms,
                        "popularity": avg_popularity,
                    }
                }
            }

            return_data.append(result)
        
        return return_data
    

def get_top_100(search_date):
    exists = Top100ByDate.objects.filter(date=search_date).exists()
    if exists:
        data = Top100ByDate.objects.get(date=search_date)
    else:
        data = None

    if data is not None and data.acousticness is not None:
        #data = Top100ByDate.objects.get(date=search_date)
        rank_with_title = ast.literal_eval(data.rank)#data.rank: 탑100 노래 이름
        rank_with_artist = data.rank_with_artist
        rank = []#rank: 탑100 json 형식 데이터
        # if rank_with_artist is None:
        #     print("Top100ByDate 모델에 추가된 테이블에 데이터 없음")#추가된 테이블에 데이터를 추가한다.
        #     saf = Spotify_audio_features()

        #     rank_with_artist = []
        #     rank_with_img64 = []
        #     rank_with_img300 = []
        #     rank_with_img640 = []
        #     for i in range(0, 100):
        #         searched_data = saf.get_features(rank_with_title[i], limit=1)
        #         #print(searched_data)
        #         rank_data = {
        #             "title": searched_data[0]["title"],
        #             "artist": searched_data[0]["artist"],
        #             "images": searched_data[0]["images"]
        #         }
        #         rank_with_artist.append(searched_data[0]["artist"])
        #         rank_with_img64.append(searched_data[0]["images"][2])
        #         rank_with_img300.append(searched_data[0]["images"][1])
        #         rank_with_img640.append(searched_data[0]["images"][0])
        #         rank.append(rank_data)
        #     data.rank_with_artist = rank_with_artist
        #     data.rank_with_img300 = rank_with_img300
        #     data.rank_with_img64 = rank_with_img64
        #     data.rank_with_img640 = rank_with_img640
        #     data.save()
        # else:
        rank_with_artist = ast.literal_eval(data.rank_with_artist)
        rank_with_img300 = ast.literal_eval(data.rank_with_img300)
        rank_with_img64 = ast.literal_eval(data.rank_with_img64)
        rank_with_img640 = ast.literal_eval(data.rank_with_img640)
        lastweek_rank = ast.literal_eval(data.lastweek_rank)
        for i in range(0, 100):
            if lastweek_rank[i] == '-': 
                rank_difference = lastweek_rank[i]
            else:
                rank_difference = str((i + 1) - int(lastweek_rank[i]))
            
            rank_data = {
                "title": rank_with_title[i],
                "artist": rank_with_artist[i],
                "images": [
                            rank_with_img640[i],
                            rank_with_img300[i],
                            rank_with_img64[i]
                ],
                "rank_difference": rank_difference
            }
            rank.append(rank_data)

        result = {
            "date": data.date,
            "rank": rank,
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
        if exists is False:      
            top_100, lastweek_rank = crawling_top_100(search_date)
        else:
            top_100 = ast.literal_eval(data.rank)
            lastweek_rank = ast.literal_eval(data.lastweek_rank)

        #평균 스탯을 계산한다.
        saf = Spotify_audio_features()
        acousticness = danceability = energy = liveness = loudness = valence = 0
        mode = speechiness = instrumentalness = tempo = duration_ms = popularity = 0

        rank_amount = 100
        rank = []
        rank_with_artist = []
        rank_with_img64 = []
        rank_with_img300 = []
        rank_with_img640 = []

        for i in range(0, 100):
            searched_data = saf.get_features(top_100[i], limit=1)
            if lastweek_rank[i] == '-': 
                rank_difference = lastweek_rank[i]
            else:
                rank_difference = str((i + 1) - int(lastweek_rank[i]))
            #print(searched_data)
            rank_data = {
                "title": searched_data[0]["title"],
                "artist": searched_data[0]["artist"],
                "images": searched_data[0]["images"],
                "rank_difference": rank_difference
            }
            rank_with_artist.append(searched_data[0]["artist"])
            rank_with_img64.append(searched_data[0]["images"][2])
            rank_with_img300.append(searched_data[0]["images"][1])
            rank_with_img640.append(searched_data[0]["images"][0])
            
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
            rank.append(rank_data)
        
        #print(rank_data)
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
            "date": search_date,
            "rank": rank,
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


        data = Top100ByDate.objects.get(date=search_date)
        data.acousticness=acousticness
        data.danceability=danceability
        data.energy=energy
        data.liveness=liveness
        data.loudness=loudness
        data.valence=valence
        data.mode=mode
        data.speechiness=speechiness
        data.instrumentalness=instrumentalness
        data.tempo=tempo
        data.duration_ms=duration_ms
        data. popularity=popularity
        data.rank_with_artist = rank_with_artist
        data.rank_with_img300 = rank_with_img300
        data.rank_with_img64 = rank_with_img64
        data.rank_with_img640 = rank_with_img640
        
        data.save()

        return result

def crawling_top_100(search_date):
    
    if Top100ByDate.objects.filter(date=search_date).exists():
        print(search_date, ": 이미 존재하는 날짜입니다.")
    else:
        #빌보드 Top 100 데이터 가져오기
        #날짜 타입은 YYYY-MM-DD
        url = 'https://www.billboard.com/charts/hot-100/'

        response = requests.get(f'{url}{search_date}')
        response_html = response.text


        crawling = BeautifulSoup(response_html, 'html.parser')
        class_data = 'c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only'
        top_songs = crawling.find_all(name = 'h3', id = 'title-of-a-story', class_ = class_data)
        top_100 = [song.get_text().strip() for song in top_songs]

        #top1은 top100과 클래스가 다름
        top_1_class_data = 'c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet'
        top_1_song = crawling.find_all(name = 'h3', id = 'title-of-a-story', class_ = top_1_class_data)
        top_1 = [song.get_text().strip() for song in top_1_song]

        top_100.insert(0, top_1[0])

        lastweek_rank_class_data = 'c-label a-font-primary-m lrv-u-padding-tb-050@mobile-max'
        lastweek_rank_data = crawling.find_all('span', class_ = lastweek_rank_class_data)
        lastweek_rank = [song.get_text().strip() for song in lastweek_rank_data]
        sorted_lastweek_rank = []
        length = int(len(lastweek_rank)/6)
        for i in range(0, length):
            sorted_lastweek_rank.append(lastweek_rank[i*6])

        #top1은 top100과 클래스가 다름
        lastweek_top_1_class_data = 'c-label a-font-primary-bold-l a-font-primary-m@mobile-max u-font-weight-normal@mobile-max lrv-u-padding-tb-050@mobile-max u-font-size-32@tablet'
        lastweek_top_1_song = crawling.find_all(name = 'span', class_ = lastweek_top_1_class_data)
        lastweek_top_1 = [song.get_text().strip() for song in lastweek_top_1_song]
        
        sorted_lastweek_rank.insert(0, lastweek_top_1[0])
        

        top_100_by_date = Top100ByDate(date=search_date, rank=top_100, lastweek_rank=sorted_lastweek_rank)
        top_100_by_date.save()
        print(search_date)
        return top_100, sorted_lastweek_rank

def crawling_top_100_by_period(search_date, end_date):
    start_date = search_date
    datetime_search_date = date.fromisoformat(search_date)
    datetime_end_date = date.fromisoformat(end_date) + datetime.timedelta(days=1)
    period = (datetime_end_date - datetime_search_date).days
    if period < 0:
        search_date = end_date
        end_date = start_date
        start_date = search_date
        datetime_search_date = date.fromisoformat(search_date)
        datetime_end_date = date.fromisoformat(end_date) + datetime.timedelta(days=1)
        period = (datetime_end_date - datetime_search_date).days
    while(datetime_search_date!=datetime_end_date):
        crawling_top_100(search_date)
        datetime_search_date += datetime.timedelta(days=1)
        search_date = date.isoformat(datetime_search_date)
    print("크롤링 끝")

            
def get_top_100_by_period(search_date, end_date, keyword=None):
    start_date = search_date
    datetime_search_date = date.fromisoformat(search_date)
    datetime_end_date = date.fromisoformat(end_date) + datetime.timedelta(days=1)
    period = (datetime_end_date - datetime_search_date).days
    if period < 0:
        search_date = end_date
        end_date = start_date
        start_date = search_date
        datetime_search_date = date.fromisoformat(search_date)
        datetime_end_date = date.fromisoformat(end_date) + datetime.timedelta(days=1)
        period = (datetime_end_date - datetime_search_date).days

    acousticness = danceability = energy = liveness = loudness = valence = 0
    mode = speechiness = instrumentalness = tempo = duration_ms = popularity = 0
    while(datetime_search_date!=datetime_end_date):
        print(search_date)
        if Top100ByDate.objects.filter(date=search_date).exists():
            data = Top100ByDate.objects.get(date=search_date)
            if data.acousticness is None:
                print("데이터 검색")
                get_top_100(search_date)
                data = Top100ByDate.objects.get(date=search_date)
            acousticness += data.acousticness
            danceability += data.danceability
            energy += data.energy 
            liveness += data.liveness 
            loudness += data.loudness
            valence += data.valence
            mode += data.mode
            speechiness += data.speechiness
            instrumentalness += data.instrumentalness
            tempo += data.tempo
            duration_ms += data.duration_ms
            popularity += data.popularity
        else:
            searched_data = get_top_100(search_date)
            acousticness += searched_data["averge_status"]["acousticness"]
            danceability += searched_data["averge_status"]["danceability"]
            energy += searched_data["averge_status"]["energy"]
            liveness += searched_data["averge_status"]["liveness"]
            loudness += searched_data["averge_status"]["loudness"]
            valence += searched_data["averge_status"]["valence"]
            mode += searched_data["averge_status"]["mode"]
            speechiness += searched_data["averge_status"]["speechiness"]
            instrumentalness += searched_data["averge_status"]["instrumentalness"]
            tempo += searched_data["averge_status"]["tempo"]
            duration_ms += searched_data["averge_status"]["duration_ms"]
            popularity += searched_data["averge_status"]["popularity"]
        
        datetime_search_date += datetime.timedelta(days=1)
        search_date = date.isoformat(datetime_search_date)
    
    acousticness /= period
    danceability /= period
    energy /= period
    liveness /= period
    loudness /= period
    valence /= period
    mode /= period
    speechiness /= period
    instrumentalness /= period
    tempo /= period
    duration_ms = round(duration_ms/period)
    popularity = round(popularity/period)

    result = {
        "keyword": keyword,
        "period": {
            "start_date": start_date,
            "end_date": end_date
        },
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

    if keyword is not None:
        analysis_by_keword = AnalysisByKeyword(keyword=keyword, start_date=start_date, end_date=end_date, acousticness=acousticness, 
                                        danceability=danceability, energy=energy, liveness=liveness, loudness=loudness, 
                                        valence=valence, mode=mode, speechiness=speechiness, instrumentalness=instrumentalness, 
                                        tempo=tempo, duration_ms=duration_ms, popularity=popularity)
        analysis_by_keword.save()

    return result
    
def get_top_100_by_keyword(keyword):
    keyword_to_date = keyword + "-01"
    start_date = None
    end_date = None
    datetime_format = "%Y-%m-%d"
    
    try:
        datetime.datetime.strptime(keyword_to_date, datetime_format)
        start_date = keyword_to_date
        datetime_end_date = date.fromisoformat(start_date) + relativedelta(months=1) - datetime.timedelta(days=1)
        end_date = date.isoformat(datetime_end_date)
    except:
        if keyword is None:
            return None
    
    is_in_model = AnalysisByKeyword.objects.filter(keyword=keyword).exists()
    
    #키워드가 날짜이고 데이터베이스에 존재하지 않을 경우
    if start_date is not None and is_in_model is False:
        searched_data = get_top_100_by_period(start_date, end_date)
        acousticness = searched_data["averge_status"]["acousticness"]
        danceability = searched_data["averge_status"]["danceability"]
        energy = searched_data["averge_status"]["energy"]
        liveness = searched_data["averge_status"]["liveness"]
        loudness = searched_data["averge_status"]["loudness"]
        valence = searched_data["averge_status"]["valence"]
        mode = searched_data["averge_status"]["mode"]
        speechiness = searched_data["averge_status"]["speechiness"]
        instrumentalness = searched_data["averge_status"]["instrumentalness"]
        tempo = searched_data["averge_status"]["tempo"]
        duration_ms = searched_data["averge_status"]["duration_ms"]
        popularity = searched_data["averge_status"]["popularity"]

        analysis_by_keword = AnalysisByKeyword(keyword=keyword, start_date=start_date, end_date=end_date, acousticness=acousticness, 
                                        danceability=danceability, energy=energy, liveness=liveness, loudness=loudness, 
                                        valence=valence, mode=mode, speechiness=speechiness, instrumentalness=instrumentalness, 
                                        tempo=tempo, duration_ms=duration_ms, popularity=popularity)
        analysis_by_keword.save()
    
    elif is_in_model is True:
        data = AnalysisByKeyword.objects.get(keyword=keyword)
        start_date = data.start_date
        end_date = data.end_date
        acousticness = data.acousticness
        danceability = data.danceability
        energy = data.energy
        liveness = data.liveness
        loudness = data.loudness
        valence = data.valence
        mode = data.mode
        speechiness = data.speechiness
        instrumentalness = data.instrumentalness
        tempo = data.tempo
        duration_ms = data.duration_ms
        popularity = data.popularity
    #데이터 검색 안됨
    else:
        return None

    result = {
        "keyword": keyword,
        "period": {
            "start_date": start_date,
            "end_date": end_date
        },
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

    return result



class Approximate_MusicStatus:
    def __init__(self, name='', input=0.0, number=0):
        self.name = name
        self.input = input
        self.number = number

    def approximate_status_by_input(self, search):
        
        self.name = search[0]['name']
        self.input = search[0]['input']
        length = len(search)
        self.number = 60

        for i in range(0, len(search)):
            print(search[i]['name'], ':', search[i]['input'])

        greater = json.loads(serializers.serialize('json', 
                MusicStatus.objects.filter(Q(acousticness__gt=(self.input))).order_by(self.name)))[:self.number]
        equal = json.loads(serializers.serialize('json', 
                MusicStatus.objects.filter(Q(acousticness__exact=(self.input)))))[:self.number]
        less = json.loads(serializers.serialize('json', 
                MusicStatus.objects.filter(Q(acousticness__lt=(self.input))).order_by('-' + self.name)))[:self.number]

        result = self.get_approximate(greater, equal, less)

        
        for i in range(1, length):
            self.name = search[i]['name']
            self.input = search[i]['input']
            self.number -= 10
            result = self.approximate_status_by_data(result)
            
        #print(result)
        return result

    def get_approximate(self, greater, equal, less):
        approximation_gap = []
        for i in range(0, len(greater)):
            gap = greater[i]['fields'][self.name] - self.input
            ap_gap = {'type': 'gt', 'gap': gap, 'index': i}
            approximation_gap.append(ap_gap)
        for i in range(0, len(less)):
            gap = less[i]['fields'][self.name] - self.input
            gap *=-1
            ap_gap = {'type': 'lt', 'gap': gap, 'index': i}
            approximation_gap.append(ap_gap)

        sorted_approximation_gap = sorted(approximation_gap, key = lambda x: x['gap'])[:self.number-len(equal)]
        result = []
        result.extend(equal)
        for i in range(0, self.number-len(equal)):
            index = sorted_approximation_gap[i]['index']
            if sorted_approximation_gap[i]['type'] == 'gt':
                result.append(greater[index])
            else:
                result.append(less[index])

        return result

    def approximate_status_by_data(self, data):
        greater = sorted([x for x in data if x['fields'][self.name] > self.input],
                            key = lambda x: x['fields'][self.name])[:self.number]
        equal = [x for x in data if x['fields'][self.name] == self.input][:self.number]
        less = sorted([x for x in data if x['fields'][self.name] < self.input],
                            key = lambda x: x['fields'][self.name], reverse=True)[:self.number]
        
        return self.get_approximate(greater, equal, less)

    









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

def data_mining(date):
    date_to_int = date.split(sep='-')
    date_to_int = list(map(int, date_to_int))
    saf = Spotify_audio_features()

    while date!="2022-10-30":
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