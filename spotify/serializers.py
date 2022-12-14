from dataclasses import field
from datetime import date
from rest_framework import serializers
from .models import *

class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = '__all__'

class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'
        
class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'

class StatusInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusInput
        fields = '__all__'

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = '__all__'        

class Top100ByDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Top100ByDate
        fields = '__all__'

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchTitle
        fields = '__all__'        

class AlbumImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumImage
        fields = '__all__'

class MusicStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicStatus
        fields = '__all__'

class ArtistInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistInfo
        fields = '__all__'

class ArtistTopTracksSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistTopTracks
        fields = '__all__'