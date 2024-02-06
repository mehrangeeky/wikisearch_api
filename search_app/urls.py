from django.urls import path
from search_app import views


urlpatterns = [
    path("word-frequency/", views.WordFrequencyView.as_view(), name="search-view"),
    path("history/", views.SearchHistoryLog.as_view(), name="search-log"),
]
