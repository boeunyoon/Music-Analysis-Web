from dataclasses import field
from datetime import date
from rest_framework import serializers
from .models import Date, Period, MusicStatus, SearchTitle, Top100ByDate, AlbumImage

class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = '__all__'

class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
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