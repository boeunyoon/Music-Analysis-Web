from django.urls import path
from . import views

urlpatterns = [
    path('get-top-100', views.Post_Date_Back_Song_Title),
    path('search-song', views.Post_Title_Back_Song_Status),
    path('get-status-period', views.Post_Period_Back_AVG_STATUS),
] 