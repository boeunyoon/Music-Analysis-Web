from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http.response import HttpResponse
from .serializers import *
from django.http import JsonResponse
from .util import *
from datetime import datetime

# 날짜별 Top 100
# [ {"date": "2022-10-08"} ] | url: /spotify/get-top-100
@api_view(['POST'])
def Post_Date_Back_Song_Title(request):
    if request.method == 'GET':
        return HttpResponse(status=200)
    if request.method == 'POST':
        json_data=json.loads(request.body)
        serializer = DateSerializer(data = request.data, many=True)
        if(serializer.is_valid()):
            date=json_data[0]['date']
            datetime_format = "%Y-%m-%d"
            try:
                datetime.strptime(date, datetime_format)
            except:
                print("잘못된 날짜입니다.")
                return Response(serializer.data ,status=status.HTTP_404_NOT_FOUND)
            else:
                print("날짜별 top 100 검색 중")
                top_100_data = get_top_100(date)
                top_100_json_data = json.dumps(top_100_data) #json 데이터로 변환
                print("검색 성공")
                return JsonResponse(top_100_json_data, safe=False)
            
            #return Response(serializer.data ,status=200)
        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)

# 특정 기간 동안의 top 100 평균 스탯
# [ {"start_date": "2022-10-08", "end_date": "2022-10-09"} ] | url: /spotify/get-status-period
@api_view(['POST'])
def Post_Period_Back_Avg_STATUS(request):
    if request.method == 'GET':
        return HttpResponse(status=200)
    if request.method == 'POST':
        json_data=json.loads(request.body)
        serializer = PeriodSerializer(data = request.data, many=True)
        if(serializer.is_valid()):
            start_date=json_data[0]['start_date']
            end_date=json_data[0]['end_date']
            datetime_format = "%Y-%m-%d"
            try:
                datetime.strptime(start_date, datetime_format)
                datetime.strptime(end_date, datetime_format)
            except:
                print("잘못된 기간입니다.")
                return Response(serializer.data ,status=status.HTTP_404_NOT_FOUND)
            else:
                print("특정기간 스탯평균 검색 중")
                avg_status_by_period_data = get_top_100_by_period(start_date, end_date)
                avg_status_by_period_json_data = json.dumps(avg_status_by_period_data) #json 데이터로 변환
                #print(avg_status_by_period_data)
                print("검색 성공")
                return JsonResponse(avg_status_by_period_json_data, safe=False)
            
            #return Response(serializer.data ,status=200)
        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)

# 키워드 검색
# [ {"keyword": "2022-10"} ] | url: /spotify/get-status-keyword
@api_view(['POST'])
def Post_Keyword_Back_Avg_STATUS(request):
    if request.method == 'GET':
        return HttpResponse(status=200)
    if request.method == 'POST':
        json_data=json.loads(request.body)
        serializer = KeywordSerializer(data = request.data, many=True)
        if(serializer.is_valid()):
            keyword=json_data[0]['keyword']
            searched_data = get_top_100_by_keyword(keyword)
            #검색 결과가 없으면 None을 return 한다.
            if searched_data is None: 
                print("잘못된 키워드입니다.")
                return Response(serializer.data ,status=status.HTTP_404_NOT_FOUND)
            else:
                searched_json_data = json.dumps(searched_data) #json 데이터로 변환
                print("키워드 검색 성공")
                return JsonResponse(searched_json_data, safe=False)

        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)

# 노래 추천
# [ {"track_id": "3rmo8F54jFF8OgYsqTxm5d", "artist_id": "6eUKZXaKkcviH0Ku9w2n3V", "genre": "pop"} ] | url: /spotify/get-recommendation
@api_view(['POST'])
def Post_Track_Back_Recommendation(request):
    if request.method == 'GET':
        return HttpResponse(status=200)
    if request.method == 'POST':
        json_data=json.loads(request.body)
        serializer = RecommendationSerializer(data = request.data, many=True)
        if(serializer.is_valid()):
            track_id=json_data[0]['track_id']
            artist_id=json_data[0]['artist_id']
            genre=json_data[0]['genre']
            saf = Spotify_audio_features()
            searched_data = saf.get_recommendation(track_id=track_id, artist_id=artist_id, genre=genre)
            #검색 결과가 없으면 None을 return 한다.
            if searched_data is None: 
                print("추천 실패")
                return Response(serializer.data ,status=status.HTTP_404_NOT_FOUND)
            else:
                searched_json_data = json.dumps(searched_data) #json 데이터로 변환
                #print(searched_data)
                print("추천 성공")
                return JsonResponse(searched_json_data, safe=False)

        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)

# 스탯 검색
# [ {"search": "Bad habits"} ] | url: /spotify/search-song
@api_view(['POST'])
def Post_Title_Back_Song_Status(request):
    if request.method == 'GET':
        return HttpResponse(status=200)
    if request.method == 'POST':
        json_data=json.loads(request.body)
        serializer = SearchSerializer(data = request.data, many=True)
        if(serializer.is_valid()):
            search=json_data[0]['search']
            print("검색어: ", search)
            saf = Spotify_audio_features()
            searched_data = saf.get_features(search, limit=5) #데이터 검색
            ex = [{'name': 'loudness', 'input': 0.5}]
            print(search_status_by_input(ex))
            #검색 결과가 없으면 None을 return 한다.
            if searched_data == None: 
                print("스탯 검색 실패")
                return Response(serializer.data ,status=status.HTTP_404_NOT_FOUND)
            else:
                searched_json_data = json.dumps(searched_data) #json 데이터로 변환
                print("스탯 검색 성공")
                #print(searched_json_data)
                #print(searched_data[0]["images"][0])
                return JsonResponse(searched_json_data, safe=False)

            
        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)

# 아티스트 검색
# [ {"search": "Ed Sheeran"} ] | url: /spotify/search-artist
@api_view(['POST'])
def Post_Artist_Back_Info(request):
    if request.method == 'GET':
        return HttpResponse(status=200)
    if request.method == 'POST':
        json_data=json.loads(request.body)
        serializer = SearchSerializer(data = request.data, many=True)
        if(serializer.is_valid()):
            search=json_data[0]['search']
            print("검색어: ", search)
            saf = Spotify_audio_features()
            searched_data = saf.get_artist_info(search) #데이터 검색
            
            #검색 결과가 없으면 None을 return 한다.
            if searched_data == None: 
                print("스탯 검색 실패")
                return Response(serializer.data ,status=status.HTTP_404_NOT_FOUND)

            else:
                searched_json_data = json.dumps(searched_data) #json 데이터로 변환
                print("스탯 검색 성공")
                #print(searched_data)
                return JsonResponse(searched_json_data, safe=False)

            
        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)

# 스탯 근사치 찾기
# [ {"name": "energy", "input": 0.5} ] | url: /spotify/get-approximation
@api_view(['POST'])
def Post_Status_Back_Approximation(request):
    if request.method == 'GET':
        return HttpResponse(status=200)
    if request.method == 'POST':
        json_data=json.loads(request.body)
        serializer = StatusInputSerializer(data = request.data, many=True)
        if(serializer.is_valid()):
            searched_data = search_status_by_input(json_data)
            #검색 결과가 없으면 None을 return 한다.
            if searched_data is None: 
                print("근사치 찾지 못함")
                return Response(serializer.data ,status=status.HTTP_404_NOT_FOUND)
            else:
                searched_json_data = json.dumps(searched_data) #json 데이터로 변환
                print("근사치 찾기 성공")
                #print(searched_data)
                return JsonResponse(searched_json_data, safe=False)

        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)