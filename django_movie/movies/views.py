from django.shortcuts import render
from rest_framework import status, generics, permissions, viewsets
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Actor, Review
from .serializers import (
    MovieListSerializer, 
    MovieDetailSerializer, 
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorListSerializer,
    ActorDetailSerializer
)
from .service import get_client_ip, MovieFilter, PaginationMovies
from .permissions import IsSuperUser

class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    '''Вывод списка фильмов'''
    filter_backends = (DjangoFilterBackend, )
    filterset_class = MovieFilter
    # permission_classes = [permissions.IsAuthenticated, ]
    pagination_class = PaginationMovies

    def get_queryset(self):
        movies = Movie.objects.filter(draft = False).annotate(
            rating_users = models.Count('ratings', filter = models.Q(ratings__ip = get_client_ip(self.request)))
        ).annotate(
            middle_star = (models.Sum(models.F('ratings__star'))/models.Count(models.F('ratings'))) - 1
        )
        
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            serializer_class = MovieListSerializer
        else:
            serializer_class = MovieDetailSerializer
        
        return serializer_class

# class MovieDetailView(generics.RetrieveAPIView):
#     '''Вывод фильма'''
#     queryset = Movie.objects.filter(draft = False)
#     serializer_class = MovieDetailSerializer

class ReviewDestroyView(generics.DestroyAPIView):
    '''Удаление комментария'''
    queryset = Review.objects.all()
    permission_classes = [IsSuperUser, ]

class ReviewCreateView(generics.CreateAPIView):
    '''Добаление комментария'''
    serializer_class = ReviewCreateSerializer


class AddStarRatingView(generics.CreateAPIView):
    '''Добавление рейтинга к фильму'''
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip = get_client_ip(self.request))

class ActorsListView(generics.ListAPIView):
    '''Вывод списка катеров и режиссеров'''
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer

class ActorDetailView(generics.RetrieveAPIView):
    '''Вывод конкретного актера или режиссера'''
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer