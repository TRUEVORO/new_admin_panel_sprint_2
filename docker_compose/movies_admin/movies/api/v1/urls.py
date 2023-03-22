from django.urls import path

from movies.api.v1 import MoviesDetailApi, MoviesListApi

urlpatterns = [
    path('movies/<uuid:pk>', MoviesDetailApi.as_view()),
    path('movies', MoviesListApi.as_view()),
]
