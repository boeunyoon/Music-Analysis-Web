from dataclasses import field
from datetime import date
from rest_framework import serializers
from .models import Date, MusicStatus, SearchTitle

class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = '__all__'

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchTitle
        fields = '__all__'        

class MusicStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicStatus
        fields = '__all__'