from rest_framework import serializers

from .models import (
    Movie, 
    Review, 
    Rating,
    Actor,
)

class MovieListSerializer(serializers.ModelSerializer):
    '''Список фильмов'''

    rating_users = serializers.BooleanField()
    middle_star = serializers.IntegerField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'tagline', 'category', 'rating_users', 'middle_star')
        
class ReviewCreateSerializer(serializers.ModelSerializer):
    '''Добавление отзыва'''

    class Meta:
        model = Review
        fields = '__all__'

class FilterReviewSerializer(serializers.ListSerializer):
    '''Фильтр комментариев, только parent'''

    def to_representation(self, data):
        data = data.filter(parent = None)
        return super().to_representation(data)

class RecursiveSerialzier(serializers.Serializer):
    '''Рекурсивный вывод детей'''

    def to_representation(self, value):
        serializer = ReviewSerializer(value, context=self.context)
        return serializer.data

class ActorListSerializer(serializers.ModelSerializer):
    '''Вывод списка актеров и режиссеров'''

    class Meta:
        model = Actor
        fields = ('id', 'name', 'image')

class ActorDetailSerializer(serializers.ModelSerializer):
    '''Вывод списка актеров и режиссеров'''

    class Meta:
        model = Actor
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    '''Вывод комментария'''

    children = RecursiveSerialzier(many = True)

    class Meta:
        list_serializer_class = FilterReviewSerializer
        model = Review
        fields = ('id', 'name', 'text', 'children')

class MovieDetailSerializer(serializers.ModelSerializer):
    '''Полный фильм'''

    category = serializers.SlugRelatedField(slug_field = 'name', read_only = True)
    directors = actors = ActorDetailSerializer(read_only = True, many = True)
    actors = ActorDetailSerializer(read_only = True, many = True)
    genres = serializers.SlugRelatedField(slug_field = 'name', read_only = True, many = True)
    reviews = ReviewSerializer(many = True)

    class Meta:
        model = Movie
        exclude = ('draft',)

class CreateRatingSerializer(serializers.ModelSerializer):
    '''Добавление рейтинга пользователя'''

    class Meta:
        model = Rating
        fields = ('star', 'movie')

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip = validated_data.get('ip', None),
            movie = validated_data.get('movie', None),
            defaults = {'star': validated_data.get('star')}
        )

        return rating

