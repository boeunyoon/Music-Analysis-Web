from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.http.response import HttpResponse
from .models import Date, SearchTitle
from .serializers import DateSerializer, SearchSerializer 
import json
from django.http import JsonResponse
from .util import *


# [ {"date": "2022-10-08"} ] / String 문자열 "2022-10-08"
@api_view(['POST'])
def Post_Date_Back_Song_Title(request):
    if request.method == 'GET':
        return HttpResponse(status=200)
    if request.method == 'POST':
        json_data=json.loads(request.body)
        serializer = DateSerializer(data = request.data, many=True)
        if(serializer.is_valid()):
            date=json_data[0]['date']
            song_titles = get_top_100(date)
            
            return Response(serializer.data ,status=200)
        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)

# [ {"search": "Bad habbits"} ] / String 문자열 "Bad habbits"
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
            searched_data = saf.get_features(search) #데이터 검색
            #검색 결과가 없으면 None을 return 한다.
            if searched_data == None: 
                print("검색실패")
                return Response(serializer.data ,status=status.HTTP_404_NOT_FOUND)

            else:
                searched_json_data = json.dumps(searched_data) #json 데이터로 변환
                print(searched_data[0]["artist"])
                #return Response(serializer.data ,status=status.HTTP_200_OK)
                return JsonResponse(searched_json_data, safe=False)

            
        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
