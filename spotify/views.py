from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http.response import HttpResponse
from .serializers import *
from django.http import JsonResponse
from .util import *
from datetime import datetime


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
                print("검색 중")
                top_100_data = get_top_100(date)
                top_100_json_data = json.dumps(top_100_data) #json 데이터로 변환
                print("검색 성공")
                return JsonResponse(top_100_json_data, safe=False)
            
            #return Response(serializer.data ,status=200)
        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)

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
                print("잘못된 날짜입니다.")
                return Response(serializer.data ,status=status.HTTP_404_NOT_FOUND)
            else:
                print("검색 중")
                avg_status_by_period_data = get_top_100_by_period(start_date, end_date)
                avg_status_by_period_json_data = json.dumps(avg_status_by_period_data) #json 데이터로 변환
                print(avg_status_by_period_data)
                print("검색 성공")
                return JsonResponse(avg_status_by_period_json_data, safe=False)
            
            #return Response(serializer.data ,status=200)
        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)

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
                print("검색 실패")
                return Response(serializer.data ,status=status.HTTP_404_NOT_FOUND)
            else:
                searched_json_data = json.dumps(searched_data) #json 데이터로 변환
                print("검색 성공")
                return JsonResponse(searched_json_data, safe=False)

        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)

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
            
            #검색 결과가 없으면 None을 return 한다.
            if searched_data == None: 
                print("검색 실패")
                return Response(serializer.data ,status=status.HTTP_404_NOT_FOUND)

            else:
                searched_json_data = json.dumps(searched_data) #json 데이터로 변환
                print("검색 성공")
                #print(searched_json_data)
                #print(searched_data[0]["images"][0])
                return JsonResponse(searched_json_data, safe=False)

            
        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
