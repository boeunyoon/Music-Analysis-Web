from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.http.response import HttpResponse
from .models import Date
from .serializers import DateSerializer, SearchSerializer 
import json
from .util import *

# Create your views here.
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

@api_view(['POST'])
def Post_Title_Back_Song_Status(request):
    if request.method == 'GET':
        return HttpResponse(status=200)
    if request.method == 'POST':
        json_data=json.loads(request.body)
        serializer = SearchSerializer(data = request.data, many=True)
        if(serializer.is_valid()):
            search=json_data[0]['search']
            print(search)
            saf = Spotify_audio_features()
            saf.get_features(search)

            return Response(serializer.data ,status=200)
        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)