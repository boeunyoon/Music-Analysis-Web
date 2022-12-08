from django.urls import path
from . import views

urlpatterns = [
    path('get-top-100', views.Post_Date_Back_Song_Title),
    path('search-song', views.Post_Title_Back_Song_Status),
    path('search-artist', views.Post_Artist_Back_Info),
    path('get-status-period', views.Post_Period_Back_Avg_STATUS),
    path('get-status-keyword', views.Post_Keyword_Back_Avg_STATUS),
    path('get-recommendation', views.Post_Track_Back_Recommendation),
    path('get-approximation', views.Post_Status_Back_Approximation),
    path('crawling', views.Post_Date_Crawling),
] 